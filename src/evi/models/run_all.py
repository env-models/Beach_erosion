"""Regenerate every Agent-C result: ``python -m evi.models.run_all [--data v1|v2] [--quick]``.

Writes figures/*.png + *.csv and figures/tables/C_*.csv tables (consumed by reports/C_models.md).
"""
from __future__ import annotations

import argparse
import copy
import json
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from . import protocol as P
from .baselines import (E_ALL, E_HAT, E_NB, OLS, Ctx, SF_PHIS, _needs_veq, baseline_models, e_times_diseq,
                        shorefor_forcing)
from .ml import FEATURES, Tree, ml_models

warnings.filterwarnings("ignore")
OUT_TAB = P.ROOT / "figures" / "tables"
TARGETS = ["dV_upper", "dV_total_fixed"]
SUBSETS = ["resolvable", "all"]
LEVELS = (0.5, 0.8, 0.9, 0.95)
CONFORMAL_MODELS = ["evi_general", "ppt_all", "eq_b", "lgbm", "two_stage_ml", "hybrid"]
REF_PPT = "ppt_2stage"


def add_shorefor(ev: pd.DataFrame, hy: pd.DataFrame) -> pd.DataFrame:
    parts = [shorefor_forcing(hy, ev, phi) for phi in SF_PHIS]
    return pd.concat([ev] + parts, axis=1)


def _fitpred(model, dtr, dte, ctx):
    m = copy.deepcopy(model).fit(dtr, ctx)
    return m, m.predict(dte)


def conformal_halfwidths(model, dtr, ctx, levels=LEVELS):
    """CV+-style: inner leave-one-winter-out abs residuals on the training data -> quantiles."""
    res = []
    for _, tr, te in P.lowo_splits(dtr):
        if len(tr) < 5:
            continue
        _, p = _fitpred(model, dtr.iloc[tr], dtr.iloc[te], ctx)
        res.extend(np.abs(dtr.iloc[te][ctx.target].to_numpy(float) - p))
    res = np.sort(np.asarray(res))
    n = len(res)
    return {a: float(res[min(n - 1, int(np.ceil((n + 1) * a)) - 1)]) for a in levels}


def evaluate(ev, iv, target, subset, models, splits="lowo", with_intervals=True, holdout_test=P.HOLDOUT_TEST,
             train_last=P.HOLDOUT_TRAIN_LAST):
    """Out-of-fold predictions for every model. Returns DataFrame (one row per event)."""
    d = ev[ev["resolvable"]] if subset == "resolvable" else ev
    d = d[d[target].notna()].reset_index(drop=True)  # missing target only (never filtered on its value)
    ctx = Ctx(target=target, intervals=iv)
    out = d[["event_id", "survey_start", "survey_end", "winter", "interval_days", target]].copy()
    out = out.rename(columns={target: "obs"})
    for k in models:
        out[k] = np.nan
    if splits == "lowo":
        folds = [(tr, te) for _, tr, te in P.lowo_splits(d)]
    else:
        tr, te = P.holdout_split(d, holdout_test, train_last)
        folds = [(tr, te)]
    from scipy.stats import norm
    for tr, te in folds:
        dtr, dte = d.iloc[tr], d.iloc[te]
        for k, m in models.items():
            fm, p = _fitpred(m, dtr, dte, ctx)
            out.loc[out.index[te], k] = p
            if k == "gp" and with_intervals:
                mu, sd = fm.predict(dte, return_std=True)
                for a in LEVELS:
                    z = norm.ppf(0.5 + a / 2)
                    out.loc[out.index[te], f"gp_lo{a}"] = mu - z * sd
                    out.loc[out.index[te], f"gp_hi{a}"] = mu + z * sd
            if k in CONFORMAL_MODELS and with_intervals:
                hw = conformal_halfwidths(m, dtr, ctx)
                for a in LEVELS:
                    out.loc[out.index[te], f"{k}_lo{a}"] = p - hw[a]
                    out.loc[out.index[te], f"{k}_hi{a}"] = p + hw[a]
    if splits != "lowo":
        out = out.loc[out.index[folds[0][1]]]
    return out


def metrics_table(pred, models, names, tag, target, subset, split):
    rows = []
    y = pred["obs"].to_numpy(float)
    refs = {"clim": pred["clim"].to_numpy(float), "clim_rate": pred["clim_rate"].to_numpy(float),
            "ppt": pred[REF_PPT].to_numpy(float)}
    for k in models:
        m = P.bootstrap_metrics(y, pred[k].to_numpy(float), refs)
        m.update(model=k, model_name=names[k], data=tag, target=target, subset=subset, split=split)
        rows.append(m)
    return rows


def coverage_rows(pred, tag, target, subset, split):
    rows = []
    for k in ["gp"] + CONFORMAL_MODELS:
        for a in LEVELS:
            lo, hi = f"{k}_lo{a}", f"{k}_hi{a}"
            if lo in pred:
                rows.append(dict(data=tag, target=target, subset=subset, split=split, model=k, nominal=a,
                                 n=len(pred), empirical=P.coverage(pred["obs"], pred[lo], pred[hi]),
                                 mean_width=float((pred[hi] - pred[lo]).mean())))
    return rows


# ------------------------------------------------------------------ ablations
@_needs_veq
def e_times_bin_fold(df, v_eq, e=E_HAT):
    return df[e].to_numpy(float) * (df["V_pre_total"].to_numpy(float) > v_eq)


def e_times(col, e=E_HAT):
    return lambda df: df[e].to_numpy(float) * df[col].to_numpy(float)


def e_times_bin_past(df, e=E_HAT):
    return df[e].to_numpy(float) * (df["V_anom_past"].to_numpy(float) > 0)


ABLATIONS = [
    # (question, variant key, reference key)
    ("Antecedent state (past-only anomaly): continuous vs binary", "ant_cont_past", "ant_bin_past"),
    ("Antecedent state (vs training-mean volume): continuous vs binary", "ant_cont_fold", "ant_bin_fold"),
    ("Antecedent state (continuous, past-only) vs none", "ant_cont_past", "E_hat"),
    ("Berm volume (continuous) vs none", "ant_berm", "E_hat"),
    ("Cluster count: with vs without", "ant_cont_past_clu", "ant_cont_past"),
    ("Energy: flux (sum P dt, HAT) vs Hs2 dt (HAT)", "E_pflux_hat", "E_hat"),
    ("Energy: notebook units vs Hs2 dt (HAT)", "E_nb_hat", "E_hat"),
    ("Energy: HAT-filtered vs all-storm (Hs2 dt)", "E_hat", "E_all"),
    ("Energy: HAT-filtered vs all-storm (flux)", "E_pflux_hat", "E_pflux_all"),
    ("ML: LightGBM with vs without antecedent features", "lgbm_full", "lgbm_noant"),
]


def ablation_models():
    no_ant = [f for f in FEATURES if f not in ("V_anom_past", "berm_volume_pre", "intertidal_slope_pre")]
    return {
        "E_hat": OLS([E_HAT], "E_hat"),
        "E_all": OLS([E_ALL], "E_all"),
        "E_nb_hat": OLS([E_NB], "E_nb_hat"),
        "E_pflux_hat": OLS(["E_Pflux_stormHAT_GJ_m"], "E_pflux_hat"),
        "E_pflux_all": OLS(["E_Pflux_storm_GJ_m"], "E_pflux_all"),
        "ant_bin_past": OLS([E_HAT, e_times_bin_past], "ant_bin_past"),
        "ant_cont_past": OLS([E_HAT, e_times("V_anom_past")], "ant_cont_past"),
        "ant_bin_fold": OLS([E_HAT, e_times_bin_fold], "ant_bin_fold", state_fn=True),
        "ant_cont_fold": OLS([E_HAT, e_times_diseq], "ant_cont_fold", state_fn=True),
        "ant_berm": OLS([E_HAT, e_times("berm_volume_pre")], "ant_berm"),
        "ant_cont_past_clu": OLS([E_HAT, e_times("V_anom_past"), "n_clusters"], "ant_cont_past_clu"),
        "lgbm_full": Tree("lgbm"),
        "lgbm_noant": Tree("lgbm", features=no_ant, name="LightGBM no antecedent"),
        "clim": baseline_models()["clim"],
        "clim_rate": baseline_models()["clim_rate"],
        REF_PPT: baseline_models()[REF_PPT],
    }


def run_ablations(ev, iv, tag):
    rows, target_rows = [], []
    am = ablation_models()
    for target in TARGETS:
        for subset in SUBSETS:
            pred = evaluate(ev, iv, target, subset, am, with_intervals=False)
            y = pred["obs"].to_numpy(float)
            for q, a, b in ABLATIONS:
                d = P.paired_delta_rmse(y, pred[a], pred[b])
                sa = P.bootstrap_metrics(y, pred[a], {"clim": pred["clim"]})
                sb = P.point_metrics(y, pred[b], {"clim": pred["clim"]})
                rows.append(dict(data=tag, target=target, subset=subset, question=q, variant=a, reference=b,
                                 rmse_variant=sa["rmse"], rmse_reference=sb["rmse"], **d,
                                 skill_clim_variant=sa["skill_clim"], skill_clim_reference=sb["skill_clim"]))
    # target ablation: EVI General (E_hat) on each target
    for target in ["dV_upper", "dV_total_fixed", "dV_total", "dV_lower_fixed"]:
        for subset in SUBSETS:
            pred = evaluate(ev, iv, target, subset, {"E_hat": am["E_hat"], "clim": am["clim"]}, with_intervals=False)
            m = P.bootstrap_metrics(pred["obs"], pred["E_hat"], {"clim": pred["clim"]})
            target_rows.append(dict(data=tag, target=target, subset=subset, n=m["n"], rmse=m["rmse"],
                                    r2=m["r2"], r2_lo=m["r2_lo"], r2_hi=m["r2_hi"], skill_clim=m["skill_clim"],
                                    skill_clim_lo=m["skill_clim_lo"], skill_clim_hi=m["skill_clim_hi"],
                                    obs_sd=float(pred["obs"].std(ddof=1))))
    return pd.DataFrame(rows), pd.DataFrame(target_rows)


def load_v1():
    from evi.io import load_hydro
    info = {"events": P.file_info(P.EVENTS_V1), "intervals": P.file_info(P.INTERVALS_V1)}
    ev, iv = P.load_events()
    return ev, iv, load_hydro(), info, [("holdout", P.HOLDOUT_TRAIN_LAST, P.HOLDOUT_TEST)], FEATURES, 4.224


def load_v2():
    """Agent A's v2 table (Castelle 2020 profiles w740 + hourly waves with direction)."""
    from evi.io import load_hydro  # noqa: F401
    dp = P.DATA
    ev_p, iv_p = dp / "events_trucvert_v2.parquet", dp / "intervals_trucvert_v2.parquet"
    info = {"events": P.file_info(ev_p), "intervals": P.file_info(iv_p)}
    ev, iv = P.prepare(pd.read_parquet(ev_p), pd.read_parquet(iv_p))
    info["n_imputed_pre_state_past_only"] = ev.attrs.get("n_imputed", {})
    clim = pd.read_parquet(dp / "climate_indices.parquet").dropna(subset=["nao_djfm"])
    nao = clim.groupby("winter")["nao_djfm"].first()
    # winter "2013-14" -> DJFM 2013-14 (climate_indices 'winter' = year of Jan); concurrent seasonal index
    ev["nao_winter"] = ev["winter"].map(lambda w: nao.get(float(int(w[:4]) + 1), float("nan")))
    hy = pd.read_parquet(dp / "waves_castelle2020.parquet").set_index("time")[["hs", "tp"]]
    hy = hy[hy.index >= ev["survey_start"].min() - pd.Timedelta(days=400)]
    holdouts = [("holdout", P.HOLDOUT_TRAIN_LAST, ("2013-14",)),
                ("recent", "2014-15", tuple(sorted(w for w in ev["winter"].unique() if w >= "2015-16")))]
    return ev, iv, hy, info, holdouts, FEATURES + ["mean_dir", "nao_winter"], 3.56


def load_v2c():
    from .events_v2 import DP, build
    ev, iv = build()
    info = {"built_by": "evi.models.events_v2 (Agent C) from Agent B files",
            "volumes": P.file_info(DP / "trucvert_castelle2020_volumes.parquet"),
            "profiles": P.file_info(DP / "trucvert_castelle2020_profiles.parquet"),
            "waves": P.file_info(DP / "waves_castelle2020.parquet"),
            "climate": P.file_info(DP / "climate_indices.parquet"),
            "n_events": len(ev), "n_intervals": len(iv), "hs95": ev.attrs["hs95"], "hs75": ev.attrs["hs75"]}
    hs95 = ev.attrs["hs95"]
    ev, iv = P.prepare(ev, iv)
    hy = pd.read_parquet(DP / "waves_castelle2020.parquet").set_index("time")[["hs", "tp"]]
    test = tuple(sorted(w for w in ev["winter"].unique() if w >= "2013-14"))
    holdouts = [("holdout", P.HOLDOUT_TRAIN_LAST, ("2013-14",)),
                ("recent", "2014-15", tuple(sorted(w for w in ev["winter"].unique() if w >= "2015-16")))]
    return ev, iv, hy, info, holdouts, FEATURES + ["mean_dir", "nao_interval"], hs95


def run(tag="v1", do_figs=True):
    P.seed_everything()
    t0 = time.time()
    OUT_TAB.mkdir(parents=True, exist_ok=True)
    ev, iv, hydro, info, holdouts, feats, hs95 = {"v1": load_v1, "v2": load_v2, "v2C": load_v2c}[tag]()
    ev = add_shorefor(ev, hydro)
    models = {**baseline_models(), **ml_models(feats)}
    names = {k: m.name for k, m in models.items()}
    rows, cov, preds = [], [], {}
    for target in TARGETS:
        for subset in SUBSETS:
            pl = evaluate(ev, iv, target, subset, models)
            preds[(target, subset, "lowo")] = pl
            rows += metrics_table(pl, models, names, tag, target, subset, "lowo")
            cov += coverage_rows(pl, tag, target, subset, "lowo")
            for label, train_last, test in holdouts:
                ph = evaluate(ev, iv, target, subset, models, splits="holdout", holdout_test=test, train_last=train_last)
                preds[(target, subset, label)] = ph
                if label == "holdout":
                    for w in test:
                        sub = ph[ph["winter"] == w]
                        if len(sub) >= 3:
                            rows += metrics_table(sub, models, names, tag, target, subset, f"holdout_{w}")
                            cov += coverage_rows(sub, tag, target, subset, f"holdout_{w}")
                if label != "holdout" or len(test) > 1:
                    sp = f"{label}_{test[0]}..{test[-1]}(train<= {train_last})"
                    rows += metrics_table(ph, models, names, tag, target, subset, sp)
                    cov += coverage_rows(ph, tag, target, subset, sp)
            print(f"[{tag}] {target}/{subset} done ({time.time()-t0:.0f}s)", flush=True)
    res = pd.DataFrame(rows)
    covdf = pd.DataFrame(cov)
    res.to_csv(OUT_TAB / f"C_results_{tag}.csv", index=False)
    covdf.to_csv(OUT_TAB / f"C_coverage_{tag}.csv", index=False)
    for (t, s, sp), p in preds.items():
        p.to_csv(OUT_TAB / f"C_pred_{tag}_{t}_{s}_{sp}.csv", index=False)
    abl, abl_t = run_ablations(ev, iv, tag)
    abl.to_csv(OUT_TAB / f"C_ablations_{tag}.csv", index=False)
    abl_t.to_csv(OUT_TAB / f"C_ablation_target_{tag}.csv", index=False)
    (OUT_TAB / f"C_datainfo_{tag}.json").write_text(json.dumps(info, indent=2))
    if do_figs:
        from .figures import make_all
        make_all(tag, ev, iv, preds, res, covdf, hydro, hs95, feats)
    print(f"[{tag}] finished in {time.time()-t0:.0f}s", flush=True)
    return res, covdf, abl, abl_t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="v1", choices=["v1", "v2", "v2C"])
    ap.add_argument("--no-figs", action="store_true")
    a = ap.parse_args()
    run(a.data, do_figs=not a.no_figs)


if __name__ == "__main__":
    main()


def hat_sensitivity():
    """LOWO skill of key models on the HAT = 2.14 m tables vs the superseded HAT = 1.75 m tables."""
    from .ml import ml_models as _ml
    rows = []
    keys = ["evi_general", "ppt_2stage", "harley", "eq_b", "rf"]
    for ver, (e2, i2, e1, i1) in {
        "v1": ("events_trucvert", "intervals_trucvert", "events_trucvert_hat175", "intervals_trucvert_hat175"),
        "v2": ("events_trucvert_v2", "intervals_trucvert_v2", "events_trucvert_v2_hat175", "intervals_trucvert_v2_hat175"),
    }.items():
        for hat, (ef, inf) in {"2.14": (e2, i2), "1.75": (e1, i1)}.items():
            ep, ip = P.DATA / f"{ef}.parquet", P.DATA / f"{inf}.parquet"
            if not ep.exists():
                continue
            ev, iv = P.load_events(ep, ip)
            allm = {**baseline_models(), **_ml()}
            ms = {k: allm[k] for k in keys + ["clim"]}
            for target in TARGETS:
                pred = evaluate(ev, iv, target, "resolvable", ms, with_intervals=False)
                for k in keys:
                    m = P.bootstrap_metrics(pred["obs"], pred[k], {"clim": pred["clim"]})
                    rows.append(dict(data=ver, hat_msl=hat, target=target, model=k, n=m["n"], rmse=m["rmse"],
                                     skill_clim=m["skill_clim"], skill_clim_lo=m["skill_clim_lo"],
                                     skill_clim_hi=m["skill_clim_hi"]))
    out = pd.DataFrame(rows)
    out.to_csv(OUT_TAB / "C_hat_sensitivity.csv", index=False)
    return out
