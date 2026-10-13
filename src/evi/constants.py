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
# HAT / PHMA. SHOM RAM tidal levels for Cap Ferret (pulled by Agent B): chart datum ZH = -1.98 m IGN69,
# PHMA = 4.51 m ZH = +2.53 m IGN69, mean level NM = 2.37 m ZH = +0.39 m IGN69, so PHMA - NM = 2.14 m.
# The thesis's "2.14 m IGN69" is therefore read as 2.14 m above MSL (Agent B's inference)
# [verify against thesis text p. 20]. Until 2026-10-13 this package used HAT_MSL = 2.14 - 0.39 = 1.75,
# which subtracted the 0.39 m offset twice (kept as HAT_MSL_SUPERSEDED for sensitivity runs).
HAT_IGN69: float = 2.53      # SHOM PHMA Cap Ferret, m IGN69
HAT_MSL: float = 2.14        # m in profile datum (MSL)
HAT_MSL_SUPERSEDED: float = 1.75
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
