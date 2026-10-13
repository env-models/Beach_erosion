"""Build a v2 event / interval table from Agent B's extended data (Castelle et al. 2020).

This is Agent C's own derived product (no v2 table from Agent A existed at run time). It mirrors
the v1 schema (`data/processed/events_trucvert_schema.md`) where possible; differences are listed
in reports/C_models.md. Output: figures/tables/C_events_v2C.csv, C_intervals_v2C.csv.

Inputs (read-only, documented in data/README.md by Agent B):
* trucvert_castelle2020_volumes.parquet — window `core300` (yl ∈ [−440, −160] m, the only
  window present 2003–2019), campaign `Monitoring` only (ECORS'08 daily surveys excluded),
  `vol_valid` only. Volumes over the fixed window xl ∈ [70, 170] m, MSL datum, HAT = +1.75 m.
* trucvert_castelle2020_profiles.parquet — core300 profiles for berm / slope / runup β.
* waves_castelle2020.parquet — hourly buoy-corrected hindcast Hs, Tp, Dm (2000–2019).
* data/raw/castelle2020_osf/Astronomical_Tide_TrucVert_2000-2020.nc — tide only (no surge),
  datum assumed MSL [verify]. TWL = tide + Stockdon R2% → under-estimates TWL by the surge.
* climate_indices.parquet — monthly NAO.
Sign: dV > 0 = erosion.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from evi.runup import deep_water_wavelength, deshoal, stockdon_r2
from evi.storms import count_clusters, detect_storms

from .protocol import ROOT

DP = ROOT / "data" / "processed"
TIDE_NC = ROOT / "data" / "raw" / "castelle2020_osf" / "Astronomical_Tide_TrucVert_2000-2020.nc"
HAT = 1.75
Z_TOE = 4.0
THR_START, THR_END = "2003-09-01", "2013-07-01"  # storm quantiles on pre-hold-out winters only
DEPTH_BUOY = 54.0  # m, CANDHIS 03302 depth per data/README.md
CLUSTER_GAP_H = 72


def _profile_stats(p: pd.DataFrame) -> dict:
    p = p.sort_values("xl")
    x, z = p["xl"].to_numpy(float), p["z"].to_numpy(float)
    # dune-toe proxy: landward-most crossing of +4 m going seaward (xl increases seaward)
    above = np.where(z >= Z_TOE)[0]
    x_toe = x[above.max()] if above.size else x.min()
    m = x >= x_toe
    berm = float(np.trapezoid(np.clip(z[m] - HAT, 0, Z_TOE - HAT), x[m])) if m.sum() > 1 else np.nan
    band = (z >= -1.5) & (z <= 1.5)
    slope = float(-np.polyfit(x[band], z[band], 1)[0]) if band.sum() >= 3 else np.nan
    # foreshore beta: mean slope between z = 0 and z = +4 m (landward-most crossings)
    def xcross(level):
        i = np.where((z[:-1] >= level) & (z[1:] < level))[0]
        if not i.size:
            return np.nan
        i = i[0]
        return x[i] + (z[i] - level) / (z[i] - z[i + 1]) * (x[i + 1] - x[i])
    x0, x4 = xcross(0.0), xcross(4.0)
    beta = 4.0 / (x0 - x4) if np.isfinite(x0) and np.isfinite(x4) and x0 > x4 else np.nan
    return {"berm_volume_pre": berm, "intertidal_slope_pre": slope, "beta": beta}


def load_tide() -> pd.Series:
    import xarray as xr
    d = xr.open_dataset(TIDE_NC, decode_times=False)
    t = pd.to_datetime((d["tideTime"].values - 719529.0) * 86400.0, unit="s").round("min")
    s = pd.Series(d["Tide"].values, index=t)
    return s[~s.index.duplicated()].resample("1h").mean()


def build(save: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    vol = pd.read_parquet(DP / "trucvert_castelle2020_volumes.parquet")
    vol = vol[(vol.window == "core300") & (vol.campaign == "Monitoring") & vol.vol_valid].sort_values("date")
    prof = pd.read_parquet(DP / "trucvert_castelle2020_profiles.parquet")
    prof = prof[prof.window == "core300"]
    st = {sid: _profile_stats(g) for sid, g in prof.groupby("survey_id")}
    vol = vol.assign(**{k: vol.survey_id.map(lambda s, k=k: st.get(s, {}).get(k, np.nan))
                        for k in ["berm_volume_pre", "intertidal_slope_pre", "beta"]})
    vol["beta"] = vol["beta"].ffill().bfill()

    w = pd.read_parquet(DP / "waves_castelle2020.parquet").set_index("time")[["hs", "tp", "dm"]]
    w = w[(w.index >= vol.date.min() - pd.Timedelta(days=60)) & (w.index <= vol.date.max())]
    tide = load_tide().reindex(w.index).interpolate(limit=3)
    w["tide"] = tide.to_numpy()
    hs, tp = w.hs.to_numpy(float), w.tp.to_numpy(float)
    # beta of the last survey strictly before each sample (no look-ahead)
    idx = np.searchsorted(vol.date.to_numpy(), w.index.to_numpy(), side="right") - 1
    beta = vol["beta"].to_numpy()[np.clip(idx, 0, None)]
    h0 = deshoal(hs, tp, h=DEPTH_BUOY)
    w["twl"] = w["tide"].to_numpy() + stockdon_r2(h0, deep_water_wavelength(tp), beta)
    ref = w.loc[THR_START:THR_END, "hs"]
    q95, q75 = float(ref.quantile(0.95)), float(ref.quantile(0.75))
    storms = detect_storms(hs, q95, q75)
    storm_id = np.full(len(w), -1)
    for k, s in enumerate(storms):
        storm_id[s.i0:s.i1 + 1] = k
    w["storm"] = storm_id
    nao = pd.read_parquet(DP / "climate_indices.parquet").set_index("date")["nao"]
    t_idx = w.index

    dt_h = 1.0
    E_nb = (1 / 16) * 1025 * 9.8 * hs ** 2 * dt_h / 1e6
    E_h2 = hs ** 2 * dt_h
    P = 1025 * 9.81 ** 2 * hs ** 2 * tp / (64 * np.pi) * dt_h * 3600 / 1e9  # GJ/m
    rows = []
    d = vol.reset_index(drop=True)
    for i in range(len(d) - 1):
        a, b = d.loc[i, "date"], d.loc[i + 1, "date"]
        m = (t_idx >= a) & (t_idx < b)
        sm = m & (storm_id >= 0)
        hat = sm & (w["twl"].to_numpy() >= HAT)
        ids = sorted(set(storm_id[sm]))
        ss = [storms[k] for k in ids]
        first = t_idx[storms[ids[0]].i0] if ids else a
        prev = [s for s in storms if t_idx[s.i1] < first]
        dirs = w["dm"].to_numpy()[sm]
        wts = E_h2[sm]
        mdir = float(np.degrees(np.arctan2((wts * np.sin(np.radians(dirs))).sum(), (wts * np.cos(np.radians(dirs))).sum())) % 360) if sm.any() else np.nan
        mid = a + (b - a) / 2
        nao_months = nao[(nao.index >= a.to_period("M").to_timestamp()) & (nao.index <= b)]
        rows.append(dict(
            event_id=f"TV{a:%Y%m%d}", survey_start=a, survey_end=b, interval_days=(b - a).days,
            n_storms=len(ids), n_clusters=count_clusters(ss, CLUSTER_GAP_H) if ss else 0,
            storm_hours_total=float(sm.sum() * dt_h),
            E_notebook_storm_MJh_m2=E_nb[sm].sum(), E_notebook_stormHAT_MJh_m2=E_nb[hat].sum(),
            E_Hs2dt_storm_m2h=E_h2[sm].sum(), E_Hs2dt_stormHAT_m2h=E_h2[hat].sum(),
            E_Pflux_storm_GJ_m=P[sm].sum(), E_Pflux_stormHAT_GJ_m=P[hat].sum(),
            peak_hs=float(hs[sm].max()) if sm.any() else np.nan,
            mean_tp_storm=float(tp[sm].mean()) if sm.any() else np.nan, mean_dir=mdir,
            hat_exceed_hours_storm=float(hat.sum() * dt_h),
            max_twl_storm=float(w["twl"].to_numpy()[sm].max()) if sm.any() else np.nan,
            V_pre_total=d.loc[i, "v_total"], V_pre_upper=d.loc[i, "v_upper"],
            berm_volume_pre=d.loc[i, "berm_volume_pre"], intertidal_slope_pre=d.loc[i, "intertidal_slope_pre"],
            dV_total=d.loc[i, "v_total"] - d.loc[i + 1, "v_total"],
            dV_total_fixed=d.loc[i, "v_total"] - d.loc[i + 1, "v_total"],
            dV_upper=d.loc[i, "v_upper"] - d.loc[i + 1, "v_upper"],
            dV_lower_fixed=d.loc[i, "v_lower"] - d.loc[i + 1, "v_lower"],
            days_since_last_storm=(first - t_idx[prev[-1].i1]).total_seconds() / 86400 if prev else np.nan,
            nao_interval=float(nao_months.mean()) if len(nao_months) else np.nan,
            winter=f"{mid.year if mid.month >= 7 else mid.year - 1}-{str((mid.year if mid.month >= 7 else mid.year - 1) + 1)[-2:]}",
            season={12: "DJF", 1: "DJF", 2: "DJF", 3: "MAM", 4: "MAM", 5: "MAM", 6: "JJA", 7: "JJA", 8: "JJA"}.get(mid.month, "SON"),
        ))
    iv = pd.DataFrame(rows)
    iv["V_pre_lower"] = iv["V_pre_total"] - iv["V_pre_upper"]
    ev = iv[iv.n_storms >= 1].reset_index(drop=True)
    ev.attrs.update(hs95=q95, hs75=q75)
    if save:
        out = ROOT / "figures" / "tables"
        out.mkdir(parents=True, exist_ok=True)
        ev.to_csv(out / "C_events_v2C.csv", index=False)
        iv.to_csv(out / "C_intervals_v2C.csv", index=False)
        (out / "C_events_v2C_meta.txt").write_text(
            f"Hs95={q95:.3f} m, Hs75={q75:.3f} m on {THR_START}..{THR_END}; storms={len(storms)}; "
            f"surveys={len(d)}; intervals={len(iv)}; events={len(ev)}\n")
    return ev, iv


if __name__ == "__main__":
    ev, iv = build()
    print(ev.shape, iv.shape, ev.attrs)
