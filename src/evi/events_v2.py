"""Event table v2 from Agent B's extended data (Castelle et al. 2020 surveys/waves, SHOM residual).

Run: ``python -m evi.events_v2`` -> data/processed/{events,intervals}_trucvert_v2.{parquet,csv}.
Read-only inputs (Agent B): trucvert_castelle2020_profiles.parquet (window ``w740``),
waves_castelle2020.parquet (hourly hs, tp, dm), tide_trucvert_castelle2020.parquet (tide_msl),
tide_shom_gauges.parquet (Arcachon-Eyrac residual used as surge).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .events import OUT, build_events, build_intervals
from .io import Profiles
from .storms import storm_thresholds

WINDOW = "w740"        # yl in [-700, 40] m: closest to the legacy 750 m averaging and present 2008-2019
X0, X1, DX = 30.0, 274.0, 2.0   # legacy-x grid; X0 = B's volume-window start (xl = 70 m, ~ +5 m MSL)
X_FIXED = 130.0        # legacy x of B's window end (xl = 170 m, ~ MSL); fixed volume window [X0, X_FIXED]
MAX_GAP_M = 10.0       # interior gaps <= 10 m filled linearly (as B)
SURGE_STATION = 190    # ARCACHON_EYRAC
START, END = "2008-01-01", "2019-12-31 23:00"


def load_profiles_v2() -> tuple[Profiles, pd.DataFrame]:
    """Grid B's long-format profiles on legacy x in [X0, X1]; trailing NaN beyond the first unfilled gap."""
    p = pd.read_parquet(OUT / "trucvert_castelle2020_profiles.parquet")
    p = p[p["window"] == WINDOW]
    x = np.arange(X0, X1 + DX / 2, DX)
    rows, dates, info = [], [], []
    for sid, g in p.groupby("survey_id", sort=False):
        s = pd.Series(g["z"].values, index=g["x_legacy"].values).sort_index().reindex(x)
        ok_start = np.isfinite(s.iloc[0])
        s = s.interpolate(limit=int(MAX_GAP_M / DX), limit_area="inside")
        z = s.values.copy()
        if not ok_start:
            info.append((sid, g["date"].iloc[0], False, np.nan)); continue
        n = int(np.argmin(np.isfinite(z))) if not np.isfinite(z).all() else len(z)
        z[n:] = np.nan
        rows.append(z); dates.append(g["date"].iloc[0])
        info.append((sid, g["date"].iloc[0], True, x[n - 1]))
    order = np.argsort(np.array(dates, dtype="datetime64[ns]"))
    t_unix = np.array(dates, dtype="datetime64[ns]").astype("int64")[order] / 1e9
    prof = Profiles(x=x, datenum=t_unix / 86400.0 + 719529.0, z=np.vstack(rows)[order])
    return prof, pd.DataFrame(info, columns=["survey_id", "date", "used", "x_end"])


def load_hydro_v2() -> pd.DataFrame:
    """Hourly forcing: Castelle waves (hs, tp, dm) + tide_msl + Arcachon residual (surge, 0 where missing)."""
    w = pd.read_parquet(OUT / "waves_castelle2020.parquet").set_index("time")[["hs", "tp", "dm"]]
    t = pd.read_parquet(OUT / "tide_trucvert_castelle2020.parquet").set_index("time")["tide_msl"]
    g = pd.read_parquet(OUT / "tide_shom_gauges.parquet")
    g = g[g["station"] == SURGE_STATION].set_index("time")["residual"]
    g.index = g.index.astype("datetime64[ns]")
    df = w.join(t, how="inner").loc[START:END]
    surge = g.reindex(df.index)
    df["surge"] = surge.fillna(0.0)
    df["surge_ok"] = surge.notna()
    df["wl"] = df["tide_msl"] + df["surge"]
    df = df.rename(columns={"dm": "dir"}).dropna(subset=["hs", "tp", "wl"])
    df["hs"] = df["hs"].clip(lower=0.0)  # 17 slightly negative hourly values (min -0.05 m) in the source
    df["t_unix"] = df.index.values.astype("datetime64[ns]").astype("int64") / 1e9
    return df


def main() -> None:
    prof, info = load_profiles_v2()
    hydro = load_hydro_v2()
    q_full = storm_thresholds(hydro["hs"], "2008-01-01", "2020-01-01")
    iv, meta = build_intervals(hydro, prof, dt_h=1.0, x_fixed=X_FIXED)
    ev = build_events(iv)
    for name, df in (("intervals", iv), ("events", ev)):
        df.to_parquet(OUT / f"{name}_trucvert_v2.parquet", index=False)
        df.to_csv(OUT / f"{name}_trucvert_v2.csv", index=False)
    print(meta, "quantiles 2008-2019 (q95, q75):", q_full)
    print(f"surveys w740: {len(info)}, used: {int(info.used.sum())}, dropped (no data at x={X0}): {int((~info.used).sum())}")
    print(f"hydro rows {len(hydro)}, surge missing frac {1 - hydro.surge_ok.mean():.3f}")
    print(f"intervals: {len(iv)}  events: {len(ev)}  {ev.survey_start.min()} -> {ev.survey_end.max()}")


if __name__ == "__main__":
    main()
