"""Loaders for the legacy repository data (read-only).

`datasets/Data_frame.csv`: 3-hourly WW3 Hs/Tp and MARS2D still water level
(column misleadingly named ``setup``). `datasets/TrucVert_OCA.mat`: longshore
averaged profiles on a 0.1 m cross-shore grid, MATLAB datenums.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.io

REPO = Path(__file__).resolve().parents[2]
HYDRO_CSV = REPO / "datasets" / "Data_frame.csv"
PROFILES_MAT = REPO / "datasets" / "TrucVert_OCA.mat"


def datenum_to_datetime(d: float) -> datetime:
    """Convert a MATLAB datenum to a naive UTC ``datetime``.

    MATLAB day 1 is 0000-01-01 (proleptic, with year 0), Python ordinal 1 is
    0001-01-01, hence the 366-day shift.
    """
    return datetime.fromordinal(int(d)) + timedelta(days=float(d) % 1) - timedelta(days=366)


def datenum_to_unix(d: np.ndarray) -> np.ndarray:
    """Vectorised datenum -> unix seconds (UTC). 719529 = datenum('1970-01-01')."""
    return (np.asarray(d, dtype=float) - 719529.0) * 86400.0


def datenum_to_unix_notebook(d: np.ndarray) -> np.ndarray:
    """The 2020 notebook's conversion, kept only for reproduction (§2.1 item 5).

    ``X*86400 + epoch(0001-01-01) - 365.242*86400 - 155491``; it is ~3600 s
    earlier than the exact conversion.
    """
    epoch_sec = -62135596800.0  # calendar.timegm(0001-01-01T00:00:00)
    return np.asarray(d, dtype=float) * 86400.0 + epoch_sec - 365.242 * 86400.0 - 155491.0


def load_hydro(path: Path | str = HYDRO_CSV) -> pd.DataFrame:
    """Return the 3-hourly forcing with a UTC DatetimeIndex.

    Columns: ``t_unix`` (s), ``hs`` (m), ``tp`` (s), ``wl`` (m, MARS2D tide+surge,
    the ``setup`` column of the CSV, assumed MSL-referenced like the profiles [verify]).
    """
    df = pd.read_csv(path, sep=";")
    df = df.rename(columns={"# time": "t_unix", "setup": "wl"})
    df.index = pd.to_datetime(df["t_unix"], unit="s", utc=True).dt.tz_localize(None)
    df.index.name = "time"
    return df[["t_unix", "hs", "tp", "wl"]]


@dataclass(frozen=True)
class Profiles:
    """Cross-shore profiles: ``z[i, j]`` at ``x[j]`` for survey ``i``."""

    x: np.ndarray          # (nx,) m, 0 = landward (dune) end
    datenum: np.ndarray    # (n,) MATLAB datenum
    z: np.ndarray          # (n, nx) m, MSL datum, trailing NaN beyond survey extent

    @property
    def time(self) -> pd.DatetimeIndex:
        return pd.to_datetime(datenum_to_unix(self.datenum), unit="s")

    @property
    def t_unix(self) -> np.ndarray:
        return datenum_to_unix(self.datenum)

    @property
    def last_valid(self) -> np.ndarray:
        """Index of the last finite elevation of each profile."""
        f = np.isfinite(self.z)
        return self.z.shape[1] - 1 - np.argmax(f[:, ::-1], axis=1)


def load_profiles(path: Path | str = PROFILES_MAT) -> Profiles:
    """Load ``TrucVert_OCA.mat``."""
    m = scipy.io.loadmat(str(path))
    return Profiles(x=m["x"].ravel().astype(float), datenum=m["date"].ravel().astype(float),
                    z=m["z"].astype(float))
