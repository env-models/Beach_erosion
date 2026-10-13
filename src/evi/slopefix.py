"""Alternative event tables with the fixed-band runup slope (``slope_method="band_0_3"``).

Run: ``python -m evi.slopefix`` -> data/processed/{events,intervals}_trucvert[_v2]_slopefix.{parquet,csv}
and prints the linear-model comparison (default vs slopefix) on v1. Default tables are not touched.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .constants import HAT_MSL
from .events import OUT, build_events, build_intervals
from .events_v2 import X_FIXED, load_hydro_v2, load_profiles_v2
from .features import timestep_features
from .io import load_hydro, load_profiles
from .reproduce import corrected_models


def _write(iv: pd.DataFrame, stem: str) -> pd.DataFrame:
    ev = build_events(iv)
    for name, df in (("intervals", iv), ("events", ev)):
        df.to_parquet(OUT / f"{name}_{stem}.parquet", index=False)
        df.to_csv(OUT / f"{name}_{stem}.csv", index=False)
    return ev


def main() -> None:
    h1, p1 = load_hydro(), load_profiles()
    h2, (p2, _) = load_hydro_v2(), load_profiles_v2()
    iv1, _ = build_intervals(h1, p1, slope_method="band_0_3")
    ev1 = _write(iv1, "trucvert_slopefix")
    iv2, _ = build_intervals(h2, p2, dt_h=1.0, x_fixed=X_FIXED, slope_method="band_0_3")
    ev2 = _write(iv2, "trucvert_v2_slopefix")
    print(f"slopefix: v1 events {len(ev1)}, v2 events {len(ev2)}")
    q = [50, 90, 99, 99.9]
    for tag, h, p in (("v1", h1, p1), ("v2", h2, p2)):
        for method in ("wl_to_4", "band_0_3"):
            ts = timestep_features(h, p, slope_method=method)
            v = ts["twl"].notna()
            print(f"{tag} {method}: beta pct {np.nanpercentile(ts.beta, q).round(3)} max {np.nanmax(ts.beta):.3f} | "
                  f"R2 pct {np.nanpercentile(ts.R2, q).round(2)} max {np.nanmax(ts.R2):.2f} | n R2>4 {(ts.R2 > 4).sum()} "
                  f"n TWL>6 {(ts.twl > 6).sum()} | TWL>=HAT {100 * (ts.twl[v] >= HAT_MSL).mean():.1f}% | max TWL {np.nanmax(ts.twl):.2f}")
    for tag, ivx, evx in (("default", pd.read_parquet(OUT / "intervals_trucvert.parquet"), pd.read_parquet(OUT / "events_trucvert.parquet")),
                          ("slopefix", iv1, ev1)):
        r = corrected_models(evx, ivx)["General (dV_upper, all events)"]
        print(f"v1 {tag}: General a={r['coef']['a']:.2f} b={r['coef']['b']:.2f} cal R2={r['cal']['R2']:.2f} (n={r['cal']['n']}) "
              f"val R2={r['val']['R2']:.2f} CI [{r['val_ci']['R2'][0]:.2f}, {r['val_ci']['R2'][1]:.2f}] RMSE={r['val']['RMSE']:.1f} (n={r['val']['n']}) "
              f"| events max_twl_all max {evx.max_twl_all.max():.2f}, n>6 m {(evx.max_twl_all > 6).sum()}")
        for k in ("TPTE-honest (dV_total_fixed, all events)", "PPT-honest (all events, fat label vs calib mean)"):
            r = corrected_models(evx, ivx)[k]
            print(f"   {k}: cal R2={r['cal']['R2']:.2f} val R2={r['val']['R2']:.2f} CI [{r['val_ci']['R2'][0]:.2f}, {r['val_ci']['R2'][1]:.2f}]")
    print(f"v2 slopefix events max_twl_all max {ev2.max_twl_all.max():.2f}, n>6 m {(ev2.max_twl_all > 6).sum()}")


if __name__ == "__main__":
    main()
