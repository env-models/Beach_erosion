"""Fixed evaluation protocol for Agent C (HANDOFF §3-C).

* Unit = event (survey-to-survey interval containing >= 1 storm).
* Resolvability rule (decided on survey spacing only, never on the target):
  ``resolvable = interval_days <= MAX_RESOLVABLE_DAYS`` (45 d). Results are given
  on all events and on resolvable events.
* CV = leave-one-winter-out (LOWO) on the ``winter`` column (storm year July-June
  of the interval midpoint, so autumn/summer events are grouped with the winter
  that follows them).
* Hold-out = train on winters <= 2012-13, test on 2013-14 (headline / stress
  test) and 2014-15 (reported separately).
* Metrics: RMSE, MAE, R2 (out-of-sample, around the test mean), bias
  (mean(pred - obs)), MSE skill vs references, bootstrap 95 % CIs over events
  (1000 resamples, seed 0).
* Sign convention (from the schema): dV > 0 = erosion (volume lost).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 0
N_BOOT = 1000
MAX_RESOLVABLE_DAYS = 45.0
HOLDOUT_TRAIN_LAST = "2012-13"
HOLDOUT_TEST = ("2013-14", "2014-15")

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "processed"
EVENTS_V1 = DATA / "events_trucvert.parquet"
INTERVALS_V1 = DATA / "intervals_trucvert.parquet"


def seed_everything(seed: int = SEED) -> None:
    import random
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def file_info(path: Path) -> dict:
    st = path.stat()
    n = len(pd.read_parquet(path))
    return {"path": str(path.relative_to(ROOT)), "mtime": pd.Timestamp(st.st_mtime, unit="s", tz="UTC")
            .tz_convert("Europe/Paris").strftime("%Y-%m-%d %H:%M:%S %Z"), "n_rows": n}


def past_only_anomaly(events: pd.DataFrame, intervals: pd.DataFrame, col: str = "V_pre_total",
                      window_days: float = 365.0) -> pd.Series:
    """V_pre minus the mean of the same quantity over surveys in [t - window, t).

    Uses only surveys strictly before ``survey_start`` (no look-ahead; fold-independent).
    Events with no prior survey get 0 (documented).
    """
    surveys = intervals[["survey_start", col]].drop_duplicates("survey_start").sort_values("survey_start")
    out = []
    for t, v in zip(events["survey_start"], events[col]):
        m = (surveys["survey_start"] < t) & (surveys["survey_start"] >= t - pd.Timedelta(days=window_days))
        out.append(v - surveys.loc[m, col].mean() if m.any() else 0.0)
    return pd.Series(out, index=events.index, name=f"{col}_anom_past")


def load_events(path: Path = EVENTS_V1, intervals_path: Path = INTERVALS_V1) -> tuple[pd.DataFrame, pd.DataFrame]:
    ev = pd.read_parquet(path).sort_values("survey_start").reset_index(drop=True)
    iv = pd.read_parquet(intervals_path).sort_values("survey_start").reset_index(drop=True)
    ev["resolvable"] = ev["interval_days"] <= MAX_RESOLVABLE_DAYS
    ev["V_anom_past"] = past_only_anomaly(ev, iv, "V_pre_total")
    ev["Vup_anom_past"] = past_only_anomaly(ev, iv, "V_pre_upper")
    ev["berm_anom_past"] = past_only_anomaly(ev, iv, "berm_volume_pre")
    ev["season_code"] = ev["season"].map({"DJF": 0, "MAM": 1, "JJA": 2, "SON": 3}).astype(float)
    ev["dsls"] = ev["days_since_last_storm"].fillna(ev["days_since_last_storm"].max())
    return ev, iv


# ---------------------------------------------------------------- splits
def lowo_splits(ev: pd.DataFrame):
    """Yield (winter, train_idx, test_idx) for leave-one-winter-out."""
    for w in sorted(ev["winter"].unique()):
        te = np.where(ev["winter"].values == w)[0]
        tr = np.where(ev["winter"].values != w)[0]
        yield w, tr, te


def holdout_split(ev: pd.DataFrame):
    tr = np.where(ev["winter"].values <= HOLDOUT_TRAIN_LAST)[0]
    te = np.where(np.isin(ev["winter"].values, HOLDOUT_TEST))[0]
    return tr, te


# ---------------------------------------------------------------- metrics
def _mse(y, p):
    return float(np.mean((np.asarray(y) - np.asarray(p)) ** 2))


def point_metrics(y, p, ref: dict[str, np.ndarray] | None = None) -> dict:
    y, p = np.asarray(y, float), np.asarray(p, float)
    out = {"n": len(y), "rmse": float(np.sqrt(_mse(y, p))), "mae": float(np.mean(np.abs(y - p))),
           "bias": float(np.mean(p - y))}
    sst = np.sum((y - y.mean()) ** 2)
    out["r2"] = float(1 - np.sum((y - p) ** 2) / sst) if sst > 0 else np.nan
    for k, r in (ref or {}).items():
        mr = _mse(y, r)
        out[f"skill_{k}"] = float(1 - _mse(y, p) / mr) if mr > 0 else np.nan
    return out


def bootstrap_metrics(y, p, ref: dict[str, np.ndarray] | None = None, n_boot: int = N_BOOT,
                      seed: int = SEED) -> dict:
    """Point metrics + percentile 95 % CIs from resampling events with replacement."""
    y, p = np.asarray(y, float), np.asarray(p, float)
    ref = {k: np.asarray(v, float) for k, v in (ref or {}).items()}
    base = point_metrics(y, p, ref)
    rng = np.random.default_rng(seed)
    keys = [k for k in base if k != "n"]
    samples = {k: [] for k in keys}
    n = len(y)
    for _ in range(n_boot):
        i = rng.integers(0, n, n)
        m = point_metrics(y[i], p[i], {k: v[i] for k, v in ref.items()})
        for k in keys:
            samples[k].append(m[k])
    for k in keys:
        a = np.asarray(samples[k], float)
        a = a[np.isfinite(a)]
        base[f"{k}_lo"] = float(np.percentile(a, 2.5)) if len(a) else np.nan
        base[f"{k}_hi"] = float(np.percentile(a, 97.5)) if len(a) else np.nan
    return base


def paired_delta_rmse(y, p_a, p_b, n_boot: int = N_BOOT, seed: int = SEED) -> dict:
    """RMSE(a) - RMSE(b) with a paired bootstrap 95 % CI (negative = a better)."""
    y, p_a, p_b = (np.asarray(v, float) for v in (y, p_a, p_b))
    d0 = np.sqrt(_mse(y, p_a)) - np.sqrt(_mse(y, p_b))
    rng = np.random.default_rng(seed)
    ds = []
    for _ in range(n_boot):
        i = rng.integers(0, len(y), len(y))
        ds.append(np.sqrt(_mse(y[i], p_a[i])) - np.sqrt(_mse(y[i], p_b[i])))
    return {"n": len(y), "d_rmse": float(d0), "d_lo": float(np.percentile(ds, 2.5)),
            "d_hi": float(np.percentile(ds, 97.5))}


def coverage(y, lo, hi) -> float:
    y = np.asarray(y, float)
    return float(np.mean((y >= np.asarray(lo)) & (y <= np.asarray(hi))))
