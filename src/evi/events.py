"""Build the survey-interval and event tables (clean pipeline, no notebook state).

Run: ``python -m evi.events`` (writes data/processed/{intervals,events}_trucvert.{parquet,csv}).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .constants import CALIB_END, CALIB_START, DT_HOURS, HAT_MSL
from .energy import e_density_dt, e_hs2dt, e_notebook, p_flux_dt
from .features import timestep_features
from .io import REPO, Profiles, load_hydro, load_profiles
from .profiles import berm_volume, intertidal_slope, valid_extent, volume, volume_change
from .storms import Storm, count_clusters, detect_storms, storm_mask, storm_thresholds

OUT = REPO / "data" / "processed"
CLUSTER_GAP_H = 72.0  # storms closer than this (calm hours) count as one cluster [choice, verify vs literature]


def winter_label(t: pd.Timestamp) -> str:
    """Storm-year label July-June, e.g. 2013-11-02 -> '2013-14'."""
    y = t.year if t.month >= 7 else t.year - 1
    return f"{y}-{(y + 1) % 100:02d}"


def season(t: pd.Timestamp) -> str:
    return {12: "DJF", 1: "DJF", 2: "DJF", 3: "MAM", 4: "MAM", 5: "MAM",
            6: "JJA", 7: "JJA", 8: "JJA"}.get(t.month, "SON")


def global_window(prof: Profiles, idx: np.ndarray) -> float:
    """Largest x covered by every profile in ``idx`` (fixed common window)."""
    return float(prof.x[min(valid_extent(prof.z[i]) for i in idx) - 1])


def _sum(a: np.ndarray, m: np.ndarray) -> float:
    return float(np.sum(a[m])) if m.any() else 0.0


def build_intervals(hydro: pd.DataFrame | None = None, prof: Profiles | None = None,
                    calib: tuple[str, str] = (CALIB_START, CALIB_END),
                    min_gap_h: float = 0.0) -> tuple[pd.DataFrame, dict]:
    """One row per consecutive survey pair fully inside the forcing record."""
    hydro = load_hydro() if hydro is None else hydro
    prof = load_profiles() if prof is None else prof
    thr_peak, thr_bound = storm_thresholds(hydro["hs"], *calib)
    storms = detect_storms(hydro["hs"].values, thr_peak, thr_bound,
                           min_gap_samples=int(round(min_gap_h / DT_HOURS)))
    smask = storm_mask(len(hydro), storms)
    sid = np.full(len(hydro), -1)
    for k, s in enumerate(storms):
        sid[s.i0:s.i1 + 1] = k
    ts = timestep_features(hydro, prof)
    hs, tp = hydro["hs"].values, hydro["tp"].values
    th, tpf = hydro["t_unix"].values, prof.t_unix
    exc = ts["exceed_hat"].values
    e = {"notebook": e_notebook(hs), "Hs2dt": e_hs2dt(hs), "dens": e_density_dt(hs), "Pflux": p_flux_dt(hs, tp) / 1e3}
    units = {"notebook": "MJh_m2", "Hs2dt": "m2h", "dens": "MJs_m2", "Pflux": "GJ_m"}

    inside = np.where((tpf >= th[0]) & (tpf <= th[-1]))[0]
    pairs = [(i, i + 1) for i in inside[:-1] if i + 1 in set(inside)]
    xg = global_window(prof, np.array(sorted({i for p in pairs for i in p})))
    s_end_t = np.array([th[s.i1] for s in storms])
    s_start_t = np.array([th[s.i0] for s in storms])
    rows = []
    for i, j in pairs:
        m = (th >= tpf[i]) & (th < tpf[j])
        ms, mx = m & smask, m & smask & exc
        ks = sorted(set(sid[ms]) - {-1})
        durs = [float(np.sum(sid[ms] == k) * DT_HOURS) for k in ks]
        first_t = s_start_t[ks[0]] if ks else tpf[i]
        prev = s_end_t[s_end_t < first_t]
        dv = volume_change(prof.x, prof.z[i], prof.z[j])
        dvg = volume_change(prof.x, prof.z[i], prof.z[j], x_max=xg)
        r = {
            "survey_start": pd.Timestamp(tpf[i], unit="s"), "survey_end": pd.Timestamp(tpf[j], unit="s"),
            "p_start": i, "p_end": j, "interval_days": (tpf[j] - tpf[i]) / 86400.0,
            "n_storms": len(ks),
            "n_clusters": count_clusters([storms[k] for k in ks], int(CLUSTER_GAP_H / DT_HOURS)),
            "storm_hours_total": float(ms.sum() * DT_HOURS),
            "storm_durations_h": ";".join(f"{d:g}" for d in durs),
            "storm_straddles_survey": bool(any(storms[k].i0 < np.argmax(m) or th[storms[k].i1] >= tpf[j] for k in ks)),
        }
        for name, arr in e.items():
            r[f"E_{name}_storm_{units[name]}"] = _sum(arr, ms)
            r[f"E_{name}_stormHAT_{units[name]}"] = _sum(arr, mx)
        r.update({
            "peak_hs": float(hs[ms].max()) if ms.any() else np.nan,
            "mean_tp_storm": float(tp[ms].mean()) if ms.any() else np.nan,
            "mean_dir": np.nan,
            "hat_exceed_hours_storm": float(mx.sum() * DT_HOURS),
            "hat_exceed_hours_all": float((m & exc).sum() * DT_HOURS),
            "max_twl_all": float(np.nanmax(ts["twl"].values[m])) if m.any() else np.nan,
            "max_twl_storm": float(np.nanmax(ts["twl"].values[ms])) if ms.any() else np.nan,
            "max_wl": float(hydro["wl"].values[m].max()),
            "V_pre_total": volume(prof.x, prof.z[i], xg),
            "V_pre_upper": volume(prof.x, prof.z[i], xg, HAT_MSL),
            "berm_volume_pre": berm_volume(prof.x, prof.z[i]),
            "intertidal_slope_pre": intertidal_slope(prof.x, prof.z[i]),
            "dV_total": dv["total"], "dV_upper": dv["upper"], "dV_lower": dv["lower"], "x_window_pair": dv["x_max"],
            "dV_total_fixed": dvg["total"], "dV_upper_fixed": dvg["upper"], "dV_lower_fixed": dvg["lower"],
            "x_window_fixed": xg,
            "days_since_last_storm": (first_t - prev.max()) / 86400.0 if prev.size else np.nan,
        })
        r["V_pre_lower"] = r["V_pre_total"] - r["V_pre_upper"]
        mid = pd.Timestamp((tpf[i] + tpf[j]) / 2, unit="s")
        r["winter"] = winter_label(mid)
        r["season"] = season(mid)
        r["period"] = "calibration" if tpf[j] <= pd.Timestamp(CALIB_END).timestamp() else "validation"
        rows.append(r)
    df = pd.DataFrame(rows)
    meta = {"hs95": thr_peak, "hs75": thr_bound, "n_storms_total": len(storms), "x_window_fixed": xg,
            "calib": calib, "min_gap_h": min_gap_h}
    return df, meta


def build_events(intervals: pd.DataFrame) -> pd.DataFrame:
    """Events = intervals containing >= 1 storm, with a stable ``event_id``."""
    ev = intervals[intervals["n_storms"] >= 1].copy().reset_index(drop=True)
    ev.insert(0, "event_id", [f"TV{t:%Y%m%d}" for t in ev["survey_start"]])
    return ev


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    iv, meta = build_intervals()
    ev = build_events(iv)
    iv.to_parquet(OUT / "intervals_trucvert.parquet", index=False)
    iv.to_csv(OUT / "intervals_trucvert.csv", index=False)
    ev.to_parquet(OUT / "events_trucvert.parquet", index=False)
    ev.to_csv(OUT / "events_trucvert.csv", index=False)
    print(meta)
    print(f"intervals: {len(iv)}  events: {len(ev)}  {ev['survey_start'].min()} -> {ev['survey_end'].max()}")


if __name__ == "__main__":
    main()
