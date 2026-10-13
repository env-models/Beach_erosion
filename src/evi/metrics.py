"""Regression metrics with seeded bootstrap confidence intervals."""
from __future__ import annotations

import numpy as np


def metrics(y: np.ndarray, yhat: np.ndarray) -> dict[str, float]:
    """R (Pearson of y vs yhat), R2 (1 - SSE/SST, can be < 0 out of sample), RMSE, bias, n."""
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    r = float(np.corrcoef(y, yhat)[0, 1]) if len(y) >= 3 else float("nan")
    sst = float(np.sum((y - y.mean()) ** 2))
    r2 = 1 - float(np.sum((y - yhat) ** 2)) / sst if sst > 0 else float("nan")
    return {"R": r, "R2": r2, "RMSE": float(np.sqrt(np.mean((y - yhat) ** 2))),
            "bias": float(np.mean(yhat - y)), "n": int(len(y))}


def bootstrap_ci(y: np.ndarray, yhat: np.ndarray, n_boot: int = 2000, seed: int = 42,
                 alpha: float = 0.05) -> dict[str, tuple[float, float]]:
    """Percentile bootstrap CIs (resampling events) for R, R2 and RMSE."""
    rng = np.random.default_rng(seed)
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    acc: dict[str, list[float]] = {"R": [], "R2": [], "RMSE": []}
    for _ in range(n_boot):
        i = rng.integers(0, len(y), len(y))
        if np.unique(i).size < 3:
            continue
        m = metrics(y[i], yhat[i])
        for k in acc:
            acc[k].append(m[k])
    return {k: (float(np.nanpercentile(v, 100 * alpha / 2)), float(np.nanpercentile(v, 100 * (1 - alpha / 2))))
            for k, v in acc.items()}
