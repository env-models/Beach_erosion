"""Faithful, parameterised port of the 2020 notebook (`Storm Impact Indicator_2.ipynb`).

With ``NotebookOptions()`` defaults the code reproduces the notebook cell by cell
(cells 6, 8, 10, 14, 16, 18, 20, 23), including its quirks. Each option switches
one audited issue (HANDOFF §2.1) to its corrected behaviour so that the effect of
every fix on the metrics can be isolated.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace

import numpy as np
import pandas as pd

from .constants import CALIB_END, CALIB_START
from .io import Profiles, datenum_to_unix, datenum_to_unix_notebook, load_hydro, load_profiles
from .profiles import landward_crossing
from .runup import stockdon_r2
from .storms import detect_storms_notebook

_trapz = getattr(np, "trapezoid", None) or np.trapz


@dataclass(frozen=True)
class NotebookOptions:
    exact_datenum: bool = False      # item 5
    threshold: float = 3.0           # item 2: notebook beta=3; HAT = 1.75 m MSL
    landward_crossing: bool = False  # items 3-4: argmin|z-level| on NaN-stripped profile vs landward crossing
    exact_deshoal: bool = False      # extra: notebook used k0 instead of dispersion k in Ks
    g: float = 9.8
    rho: float = 1025.0
    quantiles_calib_only: bool = False  # item 8: storm quantiles on the full series vs calibration only
    mean_profile_train_only: bool = False  # item 8: "fat/eroded" reference profile
    erosive_only: bool = True        # item 7: TPTE/PPT drop dV<0 (selection on the target)
    test_size: float = 0.15


def _find_nearest(a: np.ndarray, v: float) -> int:
    return int(np.abs(np.asarray(a) - v).argmin())


def indicator(hs, tp, wl, t_hs, t_prof, x, z, o: NotebookOptions) -> np.ndarray:
    """Cell 10: horizontal distance SCWmS (<0 = TWL beyond the threshold)."""
    n = len(hs)
    out = np.full(n, np.nan)
    L0 = o.g * tp ** 2 / (2 * math.pi)
    if o.exact_deshoal:
        from .runup import deshoal
        H0 = deshoal(hs, tp, 50.0, exact=True, g=o.g)
    else:
        t = 2 * math.pi * 50 / L0
        H0 = hs / np.sqrt(1 / (np.tanh(t) * (1 + 2 * t / np.sinh(2 * t))))
    pidx = np.searchsorted(t_prof, t_hs, "left") - 1
    for k in range(n):
        ele_full = z[pidx[k], :]
        ele = ele_full[~pd.isnull(ele_full)]
        if o.landward_crossing:
            xc = lambda lev: landward_crossing(x, ele_full, lev)  # noqa: E731
        else:
            xc = lambda lev: x[_find_nearest(ele, lev)]  # noqa: E731  (DIST=x not NaN-filtered)
        xf = xc(o.threshold)
        if wl[k] < ele.min():
            beta = np.nan
        else:
            beta = abs((4 - wl[k]) / (xc(wl[k]) - xc(4)))
        r2 = float(stockdon_r2(H0[k], L0[k], beta))
        twl = wl[k] + r2
        if np.isnan(twl):
            continue
        if o.landward_crossing:
            # vertical comparison is equivalent and robust: TWL above threshold <=> negative indicator
            out[k] = -1.0 if twl >= o.threshold else 1.0
        else:
            out[k] = xc(twl) - xf
    return out


def _fit_stats(y: np.ndarray, yhat: np.ndarray) -> tuple[float, float]:
    r = float(np.corrcoef(y, yhat)[1, 0]) if len(y) >= 2 else float("nan")  # n=2 gives |R|=1, as in the notebook
    return r, float(math.sqrt(np.mean((np.asarray(y) - np.asarray(yhat)) ** 2)))


def _safe_delete(a: np.ndarray, idx: list[int]) -> np.ndarray:
    """np.delete ignoring out-of-bounds indices (old-numpy behaviour seen in cell 23's warning)."""
    return np.delete(a, [i for i in idx if i < len(a)], axis=0)


def run_notebook(o: NotebookOptions = NotebookOptions(), hydro: pd.DataFrame | None = None,
                 prof: Profiles | None = None, return_events: bool = False) -> dict:
    """Run the notebook pipeline; returns fits and metrics for General/TPTE/PPT (train/test)."""
    hydro = load_hydro() if hydro is None else hydro
    prof = load_profiles() if prof is None else prof
    hs, tp, wl = (hydro[c].values.astype(float) for c in ("hs", "tp", "wl"))
    t_hs = hydro["t_unix"].values.astype(float)
    x, z = prof.x, prof.z
    tP = datenum_to_unix(prof.datenum) if o.exact_datenum else datenum_to_unix_notebook(prof.datenum)
    n = len(hs)
    n_test = math.ceil(o.test_size * n)
    n_tr = n - n_test

    # cell 6/8: mean profile and integration window
    ini = np.searchsorted(tP, t_hs[0]) - 1
    fin = np.searchsorted(tP, t_hs.max()) - 1
    k = range(ini, fin + 1)
    if o.mean_profile_train_only:
        k = [i for i in k if tP[i] <= t_hs[n_tr - 1]]
    zmoy = np.mean(z[list(k), :], axis=0)
    end = int(np.argwhere(np.isnan(zmoy)).min()) - 1
    if o.mean_profile_train_only:  # window must still be covered by every profile used
        allk = range(ini, fin + 1)
        end = min(end, int(np.argwhere(np.isnan(np.mean(z[list(allk), :], axis=0))).min()) - 1)
    int_moy = _trapz(zmoy[:end], x[:end])

    scw = indicator(hs, tp, wl, t_hs, tP, x, z, o)
    if o.quantiles_calib_only:
        sel = (t_hs >= pd.Timestamp(CALIB_START).timestamp()) & (t_hs < pd.Timestamp(CALIB_END).timestamp())
        hs_q = hs.copy()
        start, stop, s1, s2 = _storms_with_thresholds(hs, np.quantile(hs[sel], .95), np.quantile(hs[sel], .75))
    else:
        start, stop, s1, s2 = detect_storms_notebook(hs)

    def energies_volumes(lo: int, hi: int, En: np.ndarray, t_seg: np.ndarray, test: bool):
        i0 = np.searchsorted(tP, t_seg.min())
        i1 = np.searchsorted(tP, t_seg.max()) - 1
        rng_e = range(i0, i1) if test else range(i0, i1 - 1)
        En_sum = np.array([En[np.searchsorted(t_seg, tP[i]):np.searchsorted(t_seg, tP[i + 1])].sum()
                           for i in rng_e]) / 1e6
        Int = np.array([_trapz(z[i, :end], x[:end]) for i in range(i0, i1)])
        V = Int[:-1] - Int[1:]
        return En_sum, V, Int[:-1], i0

    out: dict = {"seuil1": s1, "seuil2": s2, "n_storms": len(start), "end_index": end,
                 "x_window": float(x[end - 1]), "int_moy": float(int_moy), "n_train_samples": n_tr}
    # cell 16 (no filter)
    En0 = (1 / 16 * o.rho * o.g * hs[:n_tr] ** 2) * 3
    e, v, _, _ = energies_volumes(0, n_tr, En0, t_hs[:n_tr], False)
    p = np.polyfit(e, v, 1)
    out["nofilter_train"] = dict(zip(("a", "b"), p)) | dict(zip(("R", "RMSE"), _fit_stats(v, e * p[0] + p[1]))) | {"n": len(e)}

    # cells 18/20: storm + indicator filter on train
    Hs0 = np.zeros(n_tr)
    for a, b in zip(start, stop):
        if b < n_tr:
            Hs0[a:b] = hs[a:b]
    En = np.zeros(n_tr)
    ind = [i for i in range(n_tr) if scw[i] < 0]
    En[ind] = (1 / 16 * o.rho * o.g * Hs0[ind] ** 2) * 3
    e, v, Int, i0 = energies_volumes(0, n_tr, En, t_hs[:n_tr], False)
    lab = np.where(Int > int_moy, 1.0, np.where(Int < int_moy, 0.0, 1.0))
    pre_t = tP[i0:i0 + len(v)]
    keep = e != 0
    e_g, v_g = e[keep], v[keep]
    p = np.polyfit(e_g, v_g, 1)
    out["general_train"] = {"a": p[0], "b": p[1], **dict(zip(("R", "RMSE"), _fit_stats(v_g, e_g * p[0] + p[1]))), "n": len(e_g)}
    ero = (v_g >= 0) if o.erosive_only else np.ones(len(v_g), bool)
    e_t, v_t, l_t = e_g[ero], v_g[ero], lab[keep][ero]
    p = np.polyfit(e_t, v_t, 1)
    out["tpte_train"] = {"a": p[0], "b": p[1], **dict(zip(("R", "RMSE"), _fit_stats(v_t, e_t * p[0] + p[1]))), "n": len(e_t)}
    fits = {}
    ppt = {}
    for lv, name in ((1.0, "fat"), (0.0, "eroded")):
        m = l_t == lv
        fits[lv] = np.polyfit(e_t[m], v_t[m], 1)
        R, rmse = _fit_stats(v_t[m], e_t[m] * fits[lv][0] + fits[lv][1])
        ppt[name] = {"a": fits[lv][0], "b": fits[lv][1], "R": R, "RMSE": rmse, "n": int(m.sum())}
    ntot = sum(d["n"] for d in ppt.values())
    yhat = np.where(l_t == 1.0, e_t * fits[1.0][0] + fits[1.0][1], e_t * fits[0.0][0] + fits[0.0][1])
    Rp, rmsep = _fit_stats(v_t, yhat)
    out["ppt_train"] = {**{f"{k}_{kk}": vv for k, d in ppt.items() for kk, vv in d.items()},
                        "R_weighted_nb": sum(d["R"] * d["n"] for d in ppt.values()) / ntot,
                        "RMSE_weighted_nb": sum(d["RMSE"] * d["n"] for d in ppt.values()) / ntot,
                        "R_pooled": Rp, "RMSE_pooled": rmsep, "n": ntot}
    gen_fit = (out["general_train"]["a"], out["general_train"]["b"])
    tpte_fit = (out["tpte_train"]["a"], out["tpte_train"]["b"])

    # cell 23: test
    Hs0 = np.zeros(n)
    xi = int(np.searchsorted(start, n_tr))
    for a, b in list(zip(start, stop))[xi:]:
        Hs0[a:b] = hs[a:b]
    En = np.zeros(n)
    ind = [i for i in range(n_tr, n) if scw[i] < 0]
    En[ind] = (1 / 16 * o.rho * o.g * Hs0[ind] ** 2) * 3
    En = En[n_tr:]
    e, v, Int, _ = energies_volumes(n_tr, n, En, t_hs[n_tr:], True)
    lab = np.where(Int > int_moy, 1.0, 0.0)
    zero = [i for i in range(len(e)) if e[i] == 0]
    e = np.delete(e, zero)
    v = _safe_delete(v, zero)
    lab = _safe_delete(lab, zero)
    e = e[:len(v)]
    out["general_test"] = {**dict(zip(("R", "RMSE"), _fit_stats(v, e * gen_fit[0] + gen_fit[1]))), "n": len(v)}
    ero = (v >= 0) if o.erosive_only else np.ones(len(v), bool)
    e, v, lab = e[ero], v[ero], lab[ero]
    out["tpte_test"] = {**dict(zip(("R", "RMSE"), _fit_stats(v, e * tpte_fit[0] + tpte_fit[1]))), "n": len(v)}
    pt = {}
    for lv, name in ((1.0, "fat"), (0.0, "eroded")):
        m = lab == lv
        R, rmse = _fit_stats(v[m], e[m] * fits[lv][0] + fits[lv][1])
        pt[name] = {"R": R, "RMSE": rmse, "n": int(m.sum())}
    ntot = sum(d["n"] for d in pt.values())
    yhat = np.where(lab == 1.0, e * fits[1.0][0] + fits[1.0][1], e * fits[0.0][0] + fits[0.0][1])
    Rp, rmsep = _fit_stats(v, yhat)
    out["ppt_test"] = {**{f"{k}_{kk}": vv for k, d in pt.items() for kk, vv in d.items()},
                       "R_weighted_nb": sum(d["R"] * d["n"] for d in pt.values()) / ntot,
                       "RMSE_weighted_nb": sum(d["RMSE"] * d["n"] for d in pt.values()) / ntot,
                       "R_pooled": Rp, "RMSE_pooled": rmsep, "n": ntot,
                       "y": v.tolist(), "yhat": yhat.tolist()}
    out["split_time"] = str(pd.Timestamp(t_hs[n_tr], unit="s"))
    return out


def _storms_with_thresholds(hs: np.ndarray, s1: float, s2: float):
    """Notebook storm logic (cell 14) with externally supplied thresholds."""
    calm = np.where(hs < s2)[0]
    start, stop = set(), set()
    for i in np.where(hs[:calm.max()] > s1)[0]:
        before = calm[calm < i]
        after = calm[(calm >= i) & (calm < len(hs) - 1)]
        if before.size:
            start.add(int(before.max()))
            stop.add(int(after.min()))
    return sorted(start), sorted(stop), float(s1), float(s2)


def ablation(base: NotebookOptions = NotebookOptions()) -> list[tuple[str, NotebookOptions]]:
    """Cumulative sequence of fixes, one §2.1 item at a time."""
    steps = [("0 notebook as-is", base)]
    o = replace(base, exact_datenum=True); steps.append(("1 +exact datenum (item 5)", o))
    o = replace(o, landward_crossing=True); steps.append(("2 +landward crossing, NaN-safe (items 3-4)", o))
    o = replace(o, threshold=1.75); steps.append(("3 +HAT=1.75 m MSL threshold (item 2)", o))
    o = replace(o, exact_deshoal=True, g=9.81); steps.append(("4 +exact de-shoaling, g=9.81", o))
    o = replace(o, quantiles_calib_only=True); steps.append(("5 +storm quantiles on calibration only (item 8)", o))
    o = replace(o, mean_profile_train_only=True); steps.append(("6 +mean profile from train only (item 8)", o))
    o = replace(o, erosive_only=False); steps.append(("7 +no erosive-only filter (item 7)", o))
    return steps
