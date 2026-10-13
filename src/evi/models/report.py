"""Fill the auto-generated tables of reports/C_models.md and write model cards.

``python -m evi.models.report [v1 v2]`` — replaces text between ``<!-- AUTO:key -->`` and
``<!-- /AUTO:key -->`` markers with tables built from figures/tables/C_*.csv.
"""
from __future__ import annotations

import json
import re
import sys

import pandas as pd

from . import protocol as P
from .baselines import baseline_models
from .ml import FEATURES, GP_FEATURES, LGB_PARAMS, RF_PARAMS, XGB_PARAMS, ml_models

TAB = P.ROOT / "figures" / "tables"
REPORT = P.ROOT / "reports" / "C_models.md"
CARDS = P.ROOT / "reports" / "C_model_cards"


def _ci(r, k, f="{:.2f}"):
    return f"{f.format(r[k])} [{f.format(r[k + '_lo'])}, {f.format(r[k + '_hi'])}]"


def results_md(res, split, subset, target):
    g = res[(res.split == split) & (res.subset == subset) & (res.target == target)]
    if g.empty:
        return "_(not available)_\n"
    lines = ["| model | n | RMSE [95 % CI] | MAE | R² [95 % CI] | bias | skill vs clim [95 % CI] | skill vs clim-rate | skill vs PPT 2-stage |",
             "|---|---|---|---|---|---|---|---|---|"]
    for _, r in g.iterrows():
        lines.append(f"| {r.model_name} | {r.n} | {_ci(r, 'rmse', '{:.1f}')} | {r.mae:.1f} | {_ci(r, 'r2')} | {r.bias:+.1f} | "
                     f"{_ci(r, 'skill_clim')} | {r.skill_clim_rate:.2f} | {r.skill_ppt:.2f} |")
    return "\n".join(lines) + "\n"


def ablation_md(abl):
    lines = ["| target | subset | question | n | RMSE variant | RMSE reference | ΔRMSE (variant − ref) [95 % CI] | skill vs clim (variant / ref) |",
             "|---|---|---|---|---|---|---|---|"]
    for _, r in abl.iterrows():
        lines.append(f"| {r.target} | {r.subset} | {r.question} | {r.n} | {r.rmse_variant:.2f} | {r.rmse_reference:.2f} | "
                     f"{r.d_rmse:+.2f} [{r.d_lo:+.2f}, {r.d_hi:+.2f}] | {r.skill_clim_variant:.2f} / {r.skill_clim_reference:.2f} |")
    return "\n".join(lines) + "\n"


def target_md(t):
    lines = ["| target | subset | n | sd(obs) | RMSE | R² [95 % CI] | skill vs clim [95 % CI] |", "|---|---|---|---|---|---|---|"]
    for _, r in t.iterrows():
        lines.append(f"| {r.target} | {r.subset} | {r.n} | {r.obs_sd:.1f} | {r.rmse:.1f} | {_ci(r, 'r2')} | {_ci(r, 'skill_clim')} |")
    return "\n".join(lines) + "\n"


def coverage_md(cov):
    c = cov[cov.nominal.isin([0.8, 0.9])]
    lines = ["| target | subset | split | model | n | nominal | empirical coverage | mean width (m³/m) |", "|---|---|---|---|---|---|---|---|"]
    for _, r in c.iterrows():
        lines.append(f"| {r.target} | {r.subset} | {r.split} | {r.model} | {r.n} | {r.nominal:.2f} | {r.empirical:.2f} | {r.mean_width:.1f} |")
    return "\n".join(lines) + "\n"


def fill(tag_list):
    txt = REPORT.read_text()
    blocks = {}
    for tag in tag_list:
        f = TAB / f"C_results_{tag}.csv"
        if not f.exists():
            continue
        res = pd.read_csv(f)
        info = json.loads((TAB / f"C_datainfo_{tag}.json").read_text())
        blocks[f"datainfo_{tag}"] = "```\n" + json.dumps(info, indent=2) + "\n```\n"
        for tgt in ["dV_upper", "dV_total_fixed"]:
            for sub in ["resolvable", "all"]:
                blocks[f"lowo_{tag}_{tgt}_{sub}"] = results_md(res, "lowo", sub, tgt)
                blocks[f"w1314_{tag}_{tgt}_{sub}"] = results_md(res, "holdout_2013-14", sub, tgt)
        rec = sorted(x for x in res.split.unique() if str(x).startswith("recent_"))
        if rec:
            blocks[f"recent_{tag}"] = "".join(f"`{t}`, resolvable, split `{rec[0]}`:\n" + results_md(res, rec[0], "resolvable", t) + "\n"
                                             for t in ["dV_upper", "dV_total_fixed"])
        blocks[f"abl_{tag}"] = ablation_md(pd.read_csv(TAB / f"C_ablations_{tag}.csv"))
        blocks[f"ablt_{tag}"] = target_md(pd.read_csv(TAB / f"C_ablation_target_{tag}.csv"))
        blocks[f"cov_{tag}"] = coverage_md(pd.read_csv(TAB / f"C_coverage_{tag}.csv"))
        imp = pd.read_csv(TAB / f"C_shap_importance_{tag}.csv", index_col=0)
        blocks[f"shap_{tag}"] = "| feature | mean abs SHAP (m³/m) |\n|---|---|\n" + "\n".join(
            f"| {k} | {v:.2f} |" for k, v in imp["mean_abs_shap"].items()) + "\n"
    hf = TAB / "C_hat_sensitivity.csv"
    if hf.exists():
        h = pd.read_csv(hf)
        blocks["hat"] = "| data | target | model | n | RMSE HAT 2.14 | RMSE HAT 1.75 | skill vs clim HAT 2.14 [CI] | skill vs clim HAT 1.75 [CI] |\n|---|---|---|---|---|---|---|---|\n" + "\n".join(
            f"| {d} | {t} | {m} | {g.n.iloc[0]} | " + " | ".join(f"{g[g.hat_msl == x].rmse.iloc[0]:.2f}" if (g.hat_msl == x).any() else "–" for x in (2.14, 1.75)) + " | "
            + " | ".join(_ci(g[g.hat_msl == x].iloc[0], "skill_clim") if (g.hat_msl == x).any() else "–" for x in (2.14, 1.75)) + " |"
            for (d, t, m), g in h.groupby(["data", "target", "model"], sort=False)) + "\n"
    for k, v in blocks.items():
        pat = re.compile(rf"(<!-- AUTO:{k} -->\n)(.*?)(<!-- /AUTO:{k} -->)", re.S)
        txt = pat.sub(lambda m: m.group(1) + v + m.group(3), txt)
    REPORT.write_text(txt)
    return blocks


HYPER = {"lgbm": LGB_PARAMS, "xgb": XGB_PARAMS, "rf": RF_PARAMS}
INPUTS = {
    "clim": "none (training-fold mean of the target)",
    "clim_rate": "interval_days; rate = Σ dV / Σ days over all training-winter survey intervals (storm-free included)",
    "evi_general": "E_notebook_stormHAT_MJh_m2 (≡ ρg/16·ΣHs²Δt over storm samples with TWL ≥ HAT)",
    "ppt_all": "E_notebook_stormHAT_MJh_m2, binary state = V_pre_total > training-fold mean",
    "tpte_2stage": "E_notebook_stormHAT_MJh_m2 (classifier and erosive regression)",
    "ppt_2stage": "E_notebook_stormHAT_MJh_m2 + binary state (training-fold mean volume)",
    "harley": "E_Hs2dt_storm_m2h (all storm samples, no HAT filter)",
    "splinter": "E_Pflux_storm_GJ_m, n_clusters",
    "eq_a": "E_Hs2dt_stormHAT_m2h × (V_pre_total − V_eq), V_eq = training-fold mean",
    "eq_b": "E_Hs2dt_stormHAT_m2h, E × (V_pre_total − V_eq)",
    "shorefor": "daily Hs, Tp from datasets/Data_frame.csv → Ω, Ω_eq(φ), P^0.5 ΔΩ summed per interval; φ ∈ {15,30,60,120,240} d",
    "lgbm": ", ".join(FEATURES), "xgb": ", ".join(FEATURES), "rf": ", ".join(FEATURES),
    "gp": ", ".join(GP_FEATURES) + " (energy as log1p; all standardised)",
    "two_stage_ml": "classifier: E_Hs2dt_stormHAT, V_anom_past, berm_volume_pre; regressors: E_Hs2dt_stormHAT",
    "hybrid": "Equilibrium B inputs + LightGBM (100 trees) on " + ", ".join(FEATURES),
}
FAIL = {
    "evi_general": "Long survey intervals (> 45 d) mix storms and recovery; skill collapses when they are included.",
    "ppt_2stage": "Hard classification: a mis-classified erosive event is predicted as the mean accretion; positive bias.",
    "tpte_2stage": "Same as PPT 2-stage; erosive regression fitted on training dV > 0 only.",
    "eq_a": "No main energy term: the disequilibrium product alone cannot predict erosion of a 'normal' beach.",
    "gp": "Posterior intervals under-cover (overconfident) with n ≈ 40 training events.",
    "lgbm": "n ≈ 40 training events per fold; depth-2 trees still unstable; extrapolates flat beyond training energy range.",
    "xgb": "As LightGBM.", "rf": "Flat extrapolation beyond the training energy range (e.g. Klaus-type storms).",
    "shorefor": "Designed for shoreline position with continuous forcing; φ chosen in-sample; only 7 years of forcing (spin-up 2008).",
}


def cards(tag="v1"):
    CARDS.mkdir(parents=True, exist_ok=True)
    res = pd.read_csv(TAB / f"C_results_{tag}.csv")
    models = {**baseline_models(), **ml_models()}
    for k, m in models.items():
        g = res[(res.model == k) & (res.split.isin(["lowo", "holdout_2013-14"]))]
        rows = "\n".join(f"| {r.target} | {r.subset} | {r.split} | {r.n} | {_ci(r, 'rmse', '{:.1f}')} | {_ci(r, 'r2')} | {_ci(r, 'skill_clim')} |"
                         for _, r in g.iterrows())
        doc = (m.__doc__ or "").strip().split("\n\n")[0]
        txt = f"""# Model card — {m.name} (`{k}`)

* **Code:** `src/evi/models/{'ml' if k in ml_models() else 'baselines'}.py`; run via `python -m evi.models.run_all`.
* **Inputs:** {INPUTS.get(k, '–')}
* **Targets:** `dV_upper` (m³/m above HAT) and `dV_total_fixed` (m³/m, fixed 0–139.9 m window); > 0 = erosion.
* **Hyper-parameters:** {json.dumps(HYPER.get(k, {})) if k in HYPER else 'none / closed-form least squares' if k not in ('gp',) else 'ConstantKernel·RBF(ARD)+White, normalize_y, 5 optimizer restarts'}; fixed a priori, not tuned on test folds.
* **Seed:** {P.SEED} (numpy, sklearn, LightGBM/XGBoost `random_state`).
* **Description:** {doc or m.name}
* **Known failure modes:** {FAIL.get(k, 'Small n; see C_models.md limitations.')}

## Cross-validated results (data {tag}; LOWO = leave-one-winter-out; hold-out = trained on winters ≤ 2012-13)

| target | subset | split | n | RMSE [95 % CI] | R² [95 % CI] | skill vs climatology [95 % CI] |
|---|---|---|---|---|---|---|
{rows}
"""
        (CARDS / f"{k}.md").write_text(txt)


if __name__ == "__main__":
    tags = sys.argv[1:] or ["v1"]
    fill(tags)
    cards("v1")
