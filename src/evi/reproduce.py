"""Reproduction table (notebook as-is, ablation of fixes) and corrected EVI models.

Run: ``python -m evi.reproduce`` -> prints markdown tables, writes
``data/processed/reproduction_A.json``.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from .events import OUT, build_events, build_intervals
from .legacy import ablation, run_notebook
from .metrics import bootstrap_ci, metrics

CAL_START, VAL_START = "2009-02-09", "2013-12-01"   # thesis: calibration profiles from 2009-02-09; validation from 2013-12-01
E_COLS = {"E_notebook": "E_notebook_stormHAT_MJh_m2", "E_Hs2dt": "E_Hs2dt_stormHAT_m2h",
          "E_dens": "E_dens_stormHAT_MJs_m2", "E_Pflux": "E_Pflux_stormHAT_GJ_m"}


def split(ev: pd.DataFrame, ecol: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calibration/validation events with non-zero HAT-exceeding storm forcing (selection on X only)."""
    ev = ev[ev[ecol] > 0]
    cal = ev[(ev.survey_start >= CAL_START) & (ev.survey_end <= VAL_START)]
    val = ev[ev.survey_start >= VAL_START]
    return cal, val


def fit_eval(cal: pd.DataFrame, val: pd.DataFrame, xcol: str, ycol: str,
             group: tuple[np.ndarray, np.ndarray] | None = None) -> dict:
    """Linear fit y = a x + b on cal (per group if given), metrics on cal and val + bootstrap CI on val."""
    def fit_pred(c, v, gc=None, gv=None):
        if gc is None:
            p = np.polyfit(c[xcol], c[ycol], 1)
            return np.polyval(p, c[xcol]), np.polyval(p, v[xcol]), {"a": p[0], "b": p[1]}
        pc, pv, coefs = np.zeros(len(c)), np.zeros(len(v)), {}
        for g in (0, 1):
            p = np.polyfit(c[xcol][gc == g], c[ycol][gc == g], 1)
            pc[gc == g] = np.polyval(p, c[xcol][gc == g])
            pv[gv == g] = np.polyval(p, v[xcol][gv == g])
            coefs[f"a{g}"], coefs[f"b{g}"] = p
        return pc, pv, coefs
    pc, pv, coefs = fit_pred(cal, val, *(group or (None, None)))
    return {"coef": coefs, "cal": metrics(cal[ycol], pc), "val": metrics(val[ycol], pv),
            "val_ci": bootstrap_ci(val[ycol].values, pv)}


def corrected_models(ev: pd.DataFrame, iv: pd.DataFrame, ecol: str = E_COLS["E_notebook"]) -> dict:
    """Thesis models recomputed on the clean event table, honest and thesis-like variants."""
    cal, val = split(ev, ecol)
    # fat/eroded label: pre-storm volume vs the mean of calibration surveys only (no look-ahead)
    cal_surveys = iv[(iv.survey_start >= CAL_START) & (iv.survey_start <= VAL_START)]
    vref = cal_surveys["V_pre_total"].mean()
    g = lambda d: (d["V_pre_total"] > vref).astype(int).values  # noqa: E731  1 = fat/accreted
    ero = lambda d: d[d["dV_total_fixed"] >= 0]  # noqa: E731
    out = {
        "General (dV_upper, all events)": fit_eval(cal, val, ecol, "dV_upper"),
        "TPTE-honest (dV_total_fixed, all events)": fit_eval(cal, val, ecol, "dV_total_fixed"),
        "TPTE-thesis (dV_total_fixed, erosive only, SECONDARY)": fit_eval(ero(cal), ero(val), ecol, "dV_total_fixed"),
        "PPT-honest (all events, fat label vs calib mean)": fit_eval(cal, val, ecol, "dV_total_fixed", (g(cal), g(val))),
        "PPT-thesis (erosive only, SECONDARY)": fit_eval(ero(cal), ero(val), ecol, "dV_total_fixed", (g(ero(cal)), g(ero(val)))),
    }
    out["_meta"] = {"V_ref_calib_mean": float(vref), "n_cal": len(cal), "n_val": len(val)}
    return out


def energy_variants(ev: pd.DataFrame) -> pd.DataFrame:
    """Calibration fit / validation skill of y = aE + b for each energy definition (all events)."""
    rows = []
    for name, col in E_COLS.items():
        for scope, c in (("stormHAT", col), ("storm", col.replace("stormHAT", "storm"))):
            cal, val = split(ev, c)
            for y in ("dV_upper", "dV_total_fixed"):
                r = fit_eval(cal, val, c, y)
                rows.append({"E": name, "scope": scope, "y": y, "n_cal": r["cal"]["n"], "R2_cal": r["cal"]["R2"],
                             "n_val": r["val"]["n"], "R_val": r["val"]["R"], "R2_val": r["val"]["R2"],
                             "RMSE_val": r["val"]["RMSE"]})
    return pd.DataFrame(rows)


def main() -> None:
    res: dict = {"ablation": {}}
    for name, o in ablation():
        r = run_notebook(o)
        r["ppt_test"].pop("y"); r["ppt_test"].pop("yhat")
        res["ablation"][name] = r
    iv, meta = build_intervals()
    ev = build_events(iv)
    res["corrected"] = corrected_models(ev, iv)
    ev_tab = energy_variants(ev)
    res["energy_variants"] = ev_tab.to_dict(orient="records")
    res["meta"] = {k: (list(v) if isinstance(v, tuple) else v) for k, v in meta.items()}
    (OUT / "reproduction_A.json").write_text(json.dumps(res, indent=1, default=float))

    print("## Ablation (notebook pipeline, cumulative fixes)\n")
    print("| step | Hs95/Hs75 | General train R / RMSE (n) | General test R / RMSE (n) | TPTE train R / RMSE (n) | TPTE test R / RMSE (n) | PPT train R_w / RMSE_w (n) | PPT test R_w / R_pooled / RMSE_w (n; n_fat) |")
    print("|---|---|---|---|---|---|---|---|")
    for name, r in res["ablation"].items():
        gt, ge, tt, te, pt, pe = (r[k] for k in ("general_train", "general_test", "tpte_train", "tpte_test", "ppt_train", "ppt_test"))
        print(f"| {name} | {r['seuil1']:.2f}/{r['seuil2']:.2f} | {gt['R']:.2f} / {gt['RMSE']:.1f} ({gt['n']}) | {ge['R']:.2f} / {ge['RMSE']:.1f} ({ge['n']}) "
              f"| {tt['R']:.2f} / {tt['RMSE']:.1f} ({tt['n']}) | {te['R']:.2f} / {te['RMSE']:.1f} ({te['n']}) "
              f"| {pt['R_weighted_nb']:.2f} / {pt['RMSE_weighted_nb']:.2f} ({pt['n']}) | {pe['R_weighted_nb']:.2f} / {pe['R_pooled']:.2f} / {pe['RMSE_weighted_nb']:.2f} ({pe['n']}; {pe['fat_n']}) |")
    print("\n## Corrected models (clean event table, E = notebook units over HAT-exceeding storm hours)\n")
    print(f"meta: {res['corrected']['_meta']}\n")
    print("| model | coefficients | cal R / R2 / RMSE (n) | val R / R2 / RMSE (n) | val 95% CI R | val 95% CI R2 | val 95% CI RMSE |")
    print("|---|---|---|---|---|---|---|")
    for name, r in res["corrected"].items():
        if name.startswith("_"):
            continue
        c, v, ci = r["cal"], r["val"], r["val_ci"]
        co = ", ".join(f"{k}={x:.2f}" for k, x in r["coef"].items())
        print(f"| {name} | {co} | {c['R']:.2f} / {c['R2']:.2f} / {c['RMSE']:.1f} ({c['n']}) | {v['R']:.2f} / {v['R2']:.2f} / {v['RMSE']:.1f} ({v['n']}) "
              f"| [{ci['R'][0]:.2f}, {ci['R'][1]:.2f}] | [{ci['R2'][0]:.2f}, {ci['R2'][1]:.2f}] | [{ci['RMSE'][0]:.1f}, {ci['RMSE'][1]:.1f}] |")
    print("\n## Energy variants (y = aE + b, all events, no target filter)\n")
    print("| " + " | ".join(ev_tab.columns) + " |")
    print("|" + "---|" * len(ev_tab.columns))
    for _, row in ev_tab.iterrows():
        print("| " + " | ".join(f"{v:.2f}" if isinstance(v, float) else str(v) for v in row.values) + " |")


if __name__ == "__main__":
    main()
