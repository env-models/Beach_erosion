import numpy as np
import pandas as pd

from evi.storms import count_clusters, detect_storms, detect_storms_notebook, storm_mask, storm_thresholds


def _series():
    hs = np.full(40, 1.0)
    hs[5:10] = [3, 5, 6, 5, 3]      # storm A (peaks above 4)
    hs[12:14] = [3, 3]              # above bound but no peak -> not a storm
    hs[16:20] = [3, 4.5, 3.5, 3]    # storm B, 2-sample gap after A's end... (gap 10..15 = 6 samples)
    hs[22:24] = [5, 3]              # storm C, 2 calm samples after B
    return hs


def test_detect_storms_basic():
    s = detect_storms(_series(), thr_peak=4.0, thr_bound=2.0)
    assert [(x.i0, x.i1) for x in s] == [(5, 9), (16, 19), (22, 23)]
    assert storm_mask(40, s).sum() == 5 + 4 + 2


def test_merge_and_clusters():
    s = detect_storms(_series(), 4.0, 2.0, min_gap_samples=3)
    assert [(x.i0, x.i1) for x in s] == [(5, 9), (16, 23)]
    s0 = detect_storms(_series(), 4.0, 2.0)
    assert count_clusters(s0, 3) == 2 and count_clusters(s0, 7) == 1


def test_notebook_storm_quirk_includes_preceding_calm_sample():
    hs = _series()
    start, stop, s1, s2 = detect_storms_notebook(hs)
    assert s1 == np.quantile(hs, .95) and s2 == np.quantile(hs, .75)


def test_thresholds_respect_period():
    idx = pd.date_range("2009-01-01", periods=10, freq="D")
    hs = pd.Series(np.arange(10.0), index=idx)
    q95, q75 = storm_thresholds(hs, "2009-01-01", "2009-01-06")  # values 0..4 only
    assert q95 == np.quantile(np.arange(5.0), .95) and q75 == np.quantile(np.arange(5.0), .75)
