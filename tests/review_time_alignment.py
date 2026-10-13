"""Reviewer R (review of Agent A): survey-boundary convention mismatch between modules.

`evi.events.build_intervals` assigns a forcing sample at time t to the interval
[survey_start, survey_end) (schema: "a sample at time t belongs to interval
[survey_start, survey_end)"), but `evi.features.profile_in_force` uses the last
survey *strictly before* t (searchsorted side="left"). After the +3600 s clock fix
every survey time (all at 12:00 UTC) coincides with a forcing sample, so the first
sample of every interval is counted in interval (i -> i+1) while its slope / R2% /
TWL / HAT exceedance is computed on profile i-1.

Numerical effect on the committed v1 table is nil (no exceedance flips), but the
two conventions must agree. Fix: either `side="right"` in `profile_in_force`
(the survey at t is "in force" at t) or intervals (survey_start, survey_end].

Run explicitly: ``pytest -q tests/review_time_alignment.py`` (not matched by the
default ``test_*.py`` pattern, so it does not break the main suite).
"""
import numpy as np

from evi.events import build_intervals
from evi.features import timestep_features
from evi.io import load_hydro, load_profiles


def test_samples_in_interval_use_the_interval_pre_profile():
    hydro, prof = load_hydro(), load_profiles()
    iv, _ = build_intervals(hydro, prof)
    p_idx = timestep_features(hydro, prof)["p_idx"].values
    th = hydro["t_unix"].values
    bad = 0
    for _, r in iv.iterrows():
        m = (th >= prof.t_unix[r.p_start]) & (th < prof.t_unix[r.p_end])
        bad += int(np.sum(p_idx[m] != r.p_start))
    assert bad == 0, f"{bad} samples are counted in an interval but use another interval's pre-storm profile"
