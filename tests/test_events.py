import numpy as np
import pytest

from evi.events import build_events, build_intervals


@pytest.fixture(scope="module")
def tables():
    iv, meta = build_intervals()
    return iv, build_events(iv), meta


def test_no_target_filter_and_counts(tables):
    iv, ev, meta = tables
    assert len(ev) == (iv.n_storms >= 1).sum()
    assert (ev.dV_total < 0).any()            # accretion events are kept
    assert ev.event_id.is_unique


def test_energy_variants_are_rescalings(tables):
    _, ev, _ = tables
    r = ev.E_dens_storm_MJs_m2 / ev.E_Hs2dt_storm_m2h
    assert np.allclose(r[ev.E_Hs2dt_storm_m2h > 0], 1025 * 9.81 / 16 * 3600 / 1e6)
    assert (ev.E_notebook_stormHAT_MJh_m2 <= ev.E_notebook_storm_MJh_m2 + 1e-12).all()


def test_thresholds_close_to_thesis(tables):
    *_, meta = tables
    assert 4.0 < meta["hs95"] < 4.5 and 2.2 < meta["hs75"] < 2.6
