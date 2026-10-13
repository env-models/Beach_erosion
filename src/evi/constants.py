"""Physical constants and site datums used across the package.

All elevations are in metres relative to the profile datum (MSL at Truc Vert,
0 = +0.39 m IGN69, thesis §II-2).
"""
from __future__ import annotations

RHO: float = 1025.0          # sea-water density, kg/m3 (notebook value; thesis text says 1030)
G: float = 9.81              # gravity, m/s2 (notebook used 9.8)
RHO_NB: float = 1025.0       # notebook constants, kept for exact reproduction
G_NB: float = 9.8

IGN69_TO_MSL: float = -0.39  # z_MSL = z_IGN69 - 0.39
HAT_IGN69: float = 2.14      # PHMA (Highest Astronomical Tide) used in the thesis, m IGN69
HAT_MSL: float = HAT_IGN69 + IGN69_TO_MSL  # = +1.75 m in profile datum
BETA_NOTEBOOK: float = 3.0   # morphological threshold actually used in the 2020 notebook, m (profile datum)

DT_HOURS: float = 3.0        # wave/water-level time step in Data_frame.csv
DEPTH_SHOAL: float = 50.0    # depth (m) assumed at the WW3 output point for de-shoaling (notebook choice)
Z_SLOPE_TOP: float = 4.0     # upper bound (m) of the foreshore slope used for runup (notebook choice)

# Proxies defined in this package (documented in data/processed/events_trucvert_schema.md)
Z_DUNE_TOE_PROXY: float = 4.0     # m MSL; thesis tested dune-toe levels 4, 5, 6 m NGF [verify datum]
INTERTIDAL_BAND: tuple[float, float] = (-1.5, 1.5)  # m MSL, band for intertidal slope fit [verify vs local tidal datums]

# Calibration / validation split used by the thesis (Part III): calibration profiles
# 2009-02-09 .. 2014-01-02, validation starts 2013-12-01 (thesis §III-2-1).
CALIB_START: str = "2009-01-01"
CALIB_END: str = "2013-12-01"
