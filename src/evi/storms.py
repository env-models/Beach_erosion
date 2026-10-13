"""Storm detection: peak-over-threshold with a lower delimiting threshold.

Thesis definition (after Splinter et al. 2014; Masselink et al. 2014): a storm
occurs when Hs > Hs95% and is delimited by Hs75%.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Storm:
    """A storm as inclusive sample indices ``[i0, i1]`` into the Hs series."""

    i0: int
    i1: int

    @property
    def n(self) -> int:
        return self.i1 - self.i0 + 1


def storm_thresholds(hs: pd.Series, start: str | None = None, end: str | None = None,
                     q_peak: float = 0.95, q_bound: float = 0.75) -> tuple[float, float]:
    """Return (Hs_q_peak, Hs_q_bound) computed on ``hs[start:end)`` only (no look-ahead)."""
    sel = hs
    if start is not None:
        sel = sel[sel.index >= pd.Timestamp(start)]
    if end is not None:
        sel = sel[sel.index < pd.Timestamp(end)]
    return float(np.quantile(sel.values, q_peak)), float(np.quantile(sel.values, q_bound))


def detect_storms(hs: np.ndarray, thr_peak: float, thr_bound: float,
                  min_gap_samples: int = 0) -> list[Storm]:
    """Detect storms as maximal runs with Hs > ``thr_bound`` containing Hs > ``thr_peak``.

    Storms separated by fewer than ``min_gap_samples`` calm samples are merged
    (``0`` = no merging). Indices are inclusive.
    """
    hs = np.asarray(hs, float)
    above = hs > thr_bound
    edges = np.diff(np.concatenate([[0], above.astype(int), [0]]))
    starts, stops = np.where(edges == 1)[0], np.where(edges == -1)[0] - 1
    storms = [Storm(int(a), int(b)) for a, b in zip(starts, stops) if np.any(hs[a:b + 1] > thr_peak)]
    return merge_storms(storms, min_gap_samples)


def merge_storms(storms: list[Storm], min_gap_samples: int) -> list[Storm]:
    """Merge consecutive storms whose calm gap (samples) is < ``min_gap_samples``."""
    if min_gap_samples <= 0 or not storms:
        return list(storms)
    out = [storms[0]]
    for s in storms[1:]:
        gap = s.i0 - out[-1].i1 - 1
        if gap < min_gap_samples:
            out[-1] = Storm(out[-1].i0, s.i1)
        else:
            out.append(s)
    return out


def count_clusters(storms: list[Storm], cluster_gap_samples: int) -> int:
    """Number of clusters, a cluster being storms separated by < ``cluster_gap_samples``."""
    return len(merge_storms(storms, cluster_gap_samples)) if storms else 0


def storm_mask(n: int, storms: list[Storm]) -> np.ndarray:
    """Boolean mask of length ``n`` that is True on storm samples."""
    m = np.zeros(n, bool)
    for s in storms:
        m[s.i0:s.i1 + 1] = True
    return m


def detect_storms_notebook(hs: np.ndarray) -> tuple[list[int], list[int], float, float]:
    """Exact port of notebook cell 14 (quantiles on the FULL series; for reproduction).

    Returns ``start, stop, seuil1, seuil2``; the notebook then uses ``Hs[start:stop]``,
    i.e. it includes the last calm sample before the storm and excludes the first
    calm sample after it.
    """
    hs = np.asarray(hs, float)
    seuil1 = float(np.quantile(hs, 0.95))
    seuil2 = float(np.quantile(hs, 0.75))
    calm = np.where(hs < seuil2)[0]
    ind_last = calm.max()
    start, stop = set(), set()
    for i in np.where(hs[:ind_last] > seuil1)[0]:
        before = calm[calm < i]
        after = calm[(calm >= i) & (calm < len(hs) - 1)]  # enumerate(Hs[i:-1]) excludes last
        if before.size:
            start.add(int(before.max()))
            stop.add(int(after.min()))
    return sorted(start), sorted(stop), seuil1, seuil2
