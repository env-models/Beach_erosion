from datetime import datetime

import numpy as np
import pytest

from evi.io import datenum_to_datetime, datenum_to_unix, datenum_to_unix_notebook


def test_datenum_epoch():
    assert datenum_to_datetime(719529.0) == datetime(1970, 1, 1)
    assert datenum_to_unix(np.array([719529.0]))[0] == 0.0


def test_datenum_first_survey():
    assert datenum_to_datetime(732410.5) == datetime(2005, 4, 8, 12)
    assert datenum_to_unix(np.array([732410.5]))[0] == (datetime(2005, 4, 8, 12) - datetime(1970, 1, 1)).total_seconds()


def test_notebook_fudge_is_one_hour_early():
    d = np.array([732410.5, 736133.5])
    assert np.allclose(datenum_to_unix(d) - datenum_to_unix_notebook(d), 3599.8, atol=0.5)
