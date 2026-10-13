"""Agent-C figures. Each PNG has a CSV with exactly the plotted data next to it."""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from . import protocol as P  # noqa: E402

FIG = P.ROOT / "figures"
C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6"
INK, INK2 = "#0b0b0b", "#52514e"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#e6e5e0", "grid.linewidth": 0.6, "figure.dpi": 150})
LABEL = {"dV_upper": "ΔV upper beach (above HAT), m³/m", "dV_total_fixed": "ΔV total (fixed cross-shore window), m³/m"}


def _save(fig, name, df, tag):
    suffix = "" if tag == "v1" else f"_{tag}"
    fig.savefig(FIG / f"{name}{suffix}.png", bbox_inches="tight")
    df.to_csv(FIG / f"{name}{suffix}.csv", index=False)
    plt.close(fig)


def fig_skill(res, tag):
    keep = res[(res["subset"] == "resolvable") & (res["split"].isin(["lowo", "holdout_2013-14"]))
               & (~res["model"].isin(["clim"]))]
    fig, axes = plt.subplots(1, 2, figsize=(11, 6), sharey=True)
    order = (keep[(keep.split == "lowo") & (keep.target == "dV_upper")].sort_values("skill_clim")["model"].tolist())
    names = keep.drop_duplicates("model").set_index("model")["model_name"]
    for ax, t in zip(axes, ["dV_upper", "dV_total_fixed"]):
        for j, (sp, col, mk, off) in enumerate([("lowo", C1, "o", -0.15), ("holdout_2013-14", C2, "s", 0.15)]):
            g = keep[(keep.target == t) & (keep.split == sp)].set_index("model").loc[order]
            y = np.arange(len(order)) + off
            lab = {"lowo": "Leave-one-winter-out", "holdout_2013-14": "Hold-out winter 2013-14"}[sp]
            ax.errorbar(g["skill_clim"], y, xerr=[g["skill_clim"] - g["skill_clim_lo"], g["skill_clim_hi"] - g["skill_clim"]],
                        fmt=mk, color=col, ms=6, lw=1.5, capsize=0, label=f"{lab} (n={int(g['n'].iloc[0])})")
        ax.axvline(0, color=INK2, lw=1)
        ax.set_xlim(-1.2, 1)
        ax.set_title(LABEL[t], fontsize=10, color=INK)
        ax.set_xlabel("Skill vs climatology = 1 − MSE/MSE_clim\n(95 % bootstrap CI; axis clipped at −1.2)")
    axes[0].set_yticks(np.arange(len(order)))
    axes[0].set_yticklabels([names[m] for m in order], fontsize=8)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=2, fontsize=9, frameon=False, bbox_to_anchor=(0.6, -0.04))
    fig.suptitle(f"Skill of each model, resolvable events (interval ≤ {P.MAX_RESOLVABLE_DAYS:g} d), data {tag}", fontsize=11)
    fig.tight_layout()
    cols = ["model", "model_name", "target", "split", "n", "skill_clim", "skill_clim_lo", "skill_clim_hi", "rmse", "rmse_lo", "rmse_hi"]
    _save(fig, "fig_skill_comparison", keep[cols], tag)


def fig_energy(ev, tag):
    d = ev[["event_id", "E_Hs2dt_stormHAT_m2h", "E_notebook_stormHAT_MJh_m2", "dV_upper", "dV_total_fixed",
            "V_anom_past", "interval_days", "resolvable", "winter"]].copy()
    d["state"] = np.where(d["V_anom_past"] > 0, "accreted (above past-year mean)", "eroded (at/below past-year mean)")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, t in zip(axes, ["dV_upper", "dV_total_fixed"]):
        for st, col in [("accreted (above past-year mean)", C2), ("eroded (at/below past-year mean)", C1)]:
            for res, mk in [(True, "o"), (False, "X")]:
                g = d[(d.state == st) & (d.resolvable == res)]
                ax.scatter(g["E_Hs2dt_stormHAT_m2h"], g[t], c=col, marker=mk, s=40 if res else 70,
                           edgecolor="white", linewidth=0.8,
                           label=f"{st}{'' if res else ', interval > 45 d'}")
        for _, r in d[~d.resolvable].iterrows():
            ax.annotate(f"{r.event_id} ({r.interval_days:.0f} d)", (r["E_Hs2dt_stormHAT_m2h"], r[t]), fontsize=7,
                        color=INK2, xytext=(4, 4), textcoords="offset points")
        ax.axhline(0, color=INK2, lw=0.8)
        ax.set_xlabel("Σ Hs² Δt over storm samples with TWL ≥ HAT, m²·h")
        ax.set_ylabel(LABEL[t] + "\n(> 0 = erosion)")
    axes[0].legend(fontsize=7, frameon=False, loc="upper left")
    fig.suptitle(f"Storm energy reaching HAT vs volume change, all {len(d)} events (colour = past-only antecedent state)", fontsize=10)
    fig.tight_layout()
    _save(fig, "fig_energy_vs_dV", d, tag)


def fig_shap(ev, tag, features=None):
    import shap
    from .baselines import Ctx
    from .ml import FEATURES as _F, Tree
    FEATURES = _F  # noqa: N806
    d = ev[ev["resolvable"]].reset_index(drop=True)
    FEATURES = list(features or FEATURES)  # noqa: N806
    m = Tree("lgbm", FEATURES).fit(d, Ctx("dV_upper"))
    X = d[FEATURES].astype(float)
    sv = shap.TreeExplainer(m.m).shap_values(X)
    plt.figure()
    shap.summary_plot(sv, X, show=False, plot_size=(8, 5))
    fig = plt.gcf()
    fig.suptitle(f"SHAP, LightGBM on ΔV upper beach (m³/m), fit on all {len(d)} resolvable events (in-sample explanation)",
                 fontsize=9)
    out = pd.DataFrame(sv, columns=[f"shap_{c}" for c in FEATURES])
    out = pd.concat([d[["event_id"]], X, out], axis=1)
    _save(fig, "fig_shap_summary", out, tag)
    imp = pd.Series(np.abs(sv).mean(0), index=FEATURES).sort_values(ascending=False)
    top = imp.index[:3].tolist()
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
    for ax, f in zip(axes, top):
        ax.scatter(X[f], sv[:, FEATURES.index(f)], c=C1, s=30, edgecolor="white")
        ax.axhline(0, color=INK2, lw=0.8)
        ax.set_xlabel(f)
        ax.set_ylabel("SHAP value, m³/m")
    fig.tight_layout()
    _save(fig, "fig_shap_dependence", out[["event_id"] + top + [f"shap_{c}" for c in top]], tag)
    return imp


def fig_winter(preds, tag):
    rows = []
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    models = [("evi_general", "EVI General", C2), ("ppt_2stage", "PPT 2-stage (thesis-style)", C4),
              ("eq_b", "Equilibrium B", C3), ("rf", "Random forest", "#eda100")]
    for ax, t in zip(axes, ["dV_upper", "dV_total_fixed"]):
        p = preds[(t, "resolvable", "holdout")]
        p = p[p["winter"] == "2013-14"].sort_values("survey_start")
        x = pd.to_datetime(p["survey_end"])
        ax.plot(x, p["obs"].cumsum(), color=INK, lw=2.2, marker="o", ms=5, label="Observed")
        for k, lab, col in models:
            ax.plot(x, p[k].cumsum(), color=col, lw=1.6, marker="o", ms=3.5, label=lab)
        ax.axhline(0, color=INK2, lw=0.8)
        ax.set_ylabel("Cumulative " + LABEL[t] + "\n(> 0 = erosion)", fontsize=9)
        ax.tick_params(axis="x", rotation=30)
        q = p[["event_id", "survey_start", "survey_end", "obs"] + [k for k, *_ in models]].copy()
        q["target"] = t
        rows.append(q)
    axes[0].legend(fontsize=8, frameon=False)
    fig.suptitle("Hold-out winter 2013-14 (trained on winters ≤ 2012-13), resolvable events, cumulative over the winter", fontsize=10)
    fig.tight_layout()
    _save(fig, "fig_winter_2013_14", pd.concat(rows), tag)


def fig_calibration(cov, tag):
    c = cov[(cov["split"] == "lowo") & (cov["subset"] == "resolvable")]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
    cols = {"gp": C1, "evi_general": C2, "ppt_all": C4, "eq_b": C3, "lgbm": "#eda100", "two_stage_ml": "#e87ba4",
            "hybrid": "#008300"}
    for ax, t in zip(axes, ["dV_upper", "dV_total_fixed"]):
        ax.plot([0.4, 1], [0.4, 1], color=INK2, lw=1, ls="--", label="perfect calibration")
        for k, col in cols.items():
            g = c[(c.target == t) & (c.model == k)]
            ax.plot(g["nominal"], g["empirical"], marker="o", color=col, lw=1.5, ms=5,
                    label=("GP posterior" if k == "gp" else f"{k} (CV+ conformal)"))
        ax.set_xlabel("Nominal interval coverage")
        ax.set_title(LABEL[t], fontsize=9)
    axes[0].set_ylabel(f"Empirical coverage (LOWO, n = {int(c['n'].iloc[0])})")
    axes[0].legend(fontsize=7, frameon=False)
    fig.tight_layout()
    _save(fig, "fig_calibration", c, tag)


def fig_timeline(ev, iv, tag, hy, hs95):
    fig, axes = plt.subplots(2, 1, figsize=(12, 5.5), sharex=True, gridspec_kw={"height_ratios": [1, 1.2]})
    axes[0].plot(hy.index, hy["hs"], color=C1, lw=0.5)
    axes[0].axhline(hs95, color=C2, lw=1, ls="--", label=f"Hs95 = {hs95:.2f} m (storm peak threshold)")
    axes[0].set_ylabel("Hs, m")
    axes[0].legend(fontsize=8, frameon=False, loc="upper left")
    a = axes[1]
    ivp = iv.copy()
    ivp["mid"] = ivp["survey_start"] + (ivp["survey_end"] - ivp["survey_start"]) / 2
    ivp["has_storm"] = ivp["n_storms"] > 0
    for hs, col, lab in [(True, C2, "interval with ≥1 storm (event)"), (False, "#b9b8b2", "storm-free interval")]:
        g = ivp[ivp.has_storm == hs]
        a.bar(g["mid"], g["dV_upper"], width=g["interval_days"] * 0.95, color=col, label=lab, edgecolor="white", lw=0.3)
    a.axhline(0, color=INK2, lw=0.8)
    a.set_ylabel("ΔV upper beach, m³/m\n(> 0 = erosion)")
    a.legend(fontsize=8, frameon=False, loc="lower left")
    fig.suptitle(f"Forcing and survey-interval volume change, {iv.survey_start.min():%Y}–{iv.survey_end.max():%Y}, data {tag} (bar width = survey interval)", fontsize=10)
    fig.tight_layout()
    _save(fig, "fig_event_timeline", ivp[["survey_start", "survey_end", "interval_days", "n_storms", "dV_upper",
                                          "dV_total_fixed", "winter"]], tag)


def make_all(tag, ev, iv, preds, res, cov, hydro, hs95, features=None):
    FIG.mkdir(exist_ok=True)
    fig_skill(res, tag)
    fig_energy(ev, tag)
    imp = fig_shap(ev, tag, features)
    imp.rename("mean_abs_shap").to_csv(FIG / "tables" / f"C_shap_importance_{tag}.csv")
    fig_winter(preds, tag)
    fig_calibration(cov, tag)
    fig_timeline(ev, iv, tag, hydro, hs95)
