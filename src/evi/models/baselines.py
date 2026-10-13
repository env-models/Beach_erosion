"""Climatology, 2017 EVI and physics/empirical baselines.

Every model exposes ``fit(df_train, ctx) -> self`` and ``predict(df_test) -> np.ndarray``
where ``ctx`` carries the target name and the intervals table (for the
interval-length-scaled climatology). Nothing here looks at test targets.
Sign convention: target > 0 = erosion.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Default "energy" for the EVI family. E_notebook_stormHAT (1e6 J h m^-2) is a constant
# multiple (rho g / 16 / 1e6) of E_Hs2dt_stormHAT (m^2 h): linear fits are identical up to
# the slope's units, so the thesis model is evaluated with the notebook column for
# traceability and the physically named Hs^2 dt column is used elsewhere.
E_NB = "E_notebook_stormHAT_MJh_m2"
E_HAT = "E_Hs2dt_stormHAT_m2h"
E_ALL = "E_Hs2dt_storm_m2h"
P_ALL = "E_Pflux_storm_GJ_m"


@dataclass
class Ctx:
    target: str
    intervals: pd.DataFrame | None = None
    train_winters: tuple = ()


def _design(df: pd.DataFrame, cols: list) -> np.ndarray:
    X = np.column_stack([c(df) if callable(c) else df[c].to_numpy(float) for c in cols]) if cols else \
        np.empty((len(df), 0))
    return np.column_stack([np.ones(len(df)), X])


class Climatology:
    name = "Climatology (train mean)"

    def fit(self, df, ctx):
        self.mu = float(df[ctx.target].mean())
        return self

    def predict(self, df):
        return np.full(len(df), self.mu)


class ClimRate:
    """Interval-length-scaled climatology: (sum dV / sum days) over ALL training-winter
    survey intervals (incl. storm-free ones) x interval_days."""
    name = "Climatology (rate x interval)"

    def fit(self, df, ctx):
        iv = ctx.intervals
        iv = iv[iv["winter"].isin(set(df["winter"]))]
        self.rate = float(iv[ctx.target].sum() / iv["interval_days"].sum())
        return self

    def predict(self, df):
        return self.rate * df["interval_days"].to_numpy(float)


class OLS:
    """Ordinary least squares on a list of columns or callables (intercept included)."""

    def __init__(self, cols, name="OLS", state_fn=None):
        self.cols, self.name, self.state_fn = cols, name, state_fn

    def fit(self, df, ctx):
        self.target = ctx.target
        if self.state_fn is not None:
            self.state_fn_fit(df)
        X = _design(df, self._cols())
        self.beta, *_ = np.linalg.lstsq(X, df[ctx.target].to_numpy(float), rcond=None)
        return self

    def state_fn_fit(self, df):
        self.v_eq = float(df["V_pre_total"].mean())  # training-fold mean volume

    def _cols(self):
        return [c if not (callable(c) and getattr(c, "needs_veq", False)) else (lambda d, c=c: c(d, self.v_eq))
                for c in self.cols]

    def predict(self, df):
        return _design(df, self._cols()) @ self.beta


def _needs_veq(f):
    f.needs_veq = True
    return f


@_needs_veq
def e_times_diseq(df, v_eq, e=E_HAT):
    return df[e].to_numpy(float) * (df["V_pre_total"].to_numpy(float) - v_eq)


class PPTAllEvents:
    """'Honest' PPT: binary pre-storm state (V_pre_total above/below the TRAINING-fold mean,
    i.e. fat/thin vs the mean profile) with a separate dV = a_s E + b_s per state, fitted on
    ALL training events (no filtering on dV). Falls back to pooled if a state has < 3 events."""
    name = "PPT (binary state, all events)"

    def __init__(self, e=E_NB):
        self.e = e

    def fit(self, df, ctx):
        self.v_eq = float(df["V_pre_total"].mean())
        s = df["V_pre_total"].to_numpy() > self.v_eq
        y, E = df[ctx.target].to_numpy(float), df[self.e].to_numpy(float)
        pooled = np.polyfit(E, y, 1)
        self.coef = {k: (np.polyfit(E[s == k], y[s == k], 1) if (s == k).sum() >= 3 else pooled) for k in (True, False)}
        return self

    def predict(self, df):
        s = df["V_pre_total"].to_numpy() > self.v_eq
        E = df[self.e].to_numpy(float)
        return np.array([np.polyval(self.coef[k], e) for k, e in zip(s, E)])


class TwoStageThesis:
    """Thesis-style TPTE / PPT downstream of an erosion/accretion classifier.

    Stage 1: logistic P(dV > 0 | E [, state]) fitted on training events.
    Stage 2 (erosive branch): dV = aE + b fitted on training events with dV > 0 (TPTE), or per
    binary state (PPT). Accretive branch: mean dV of accretive training events.
    Prediction = hard classification (p >= 0.5) as in the thesis; ``soft=True`` gives
    p*erosive + (1-p)*accretive. Erosion-only fitting is on TRAINING labels only.
    """

    def __init__(self, ppt=False, soft=False, e=E_NB):
        self.ppt, self.soft, self.e = ppt, soft, e
        self.name = ("PPT" if ppt else "TPTE") + (" 2-stage soft" if soft else " 2-stage (thesis-style)")

    def fit(self, df, ctx):
        y = df[ctx.target].to_numpy(float)
        E = df[self.e].to_numpy(float)
        self.v_eq = float(df["V_pre_total"].mean())
        s = (df["V_pre_total"].to_numpy() > self.v_eq).astype(float)
        Xc = np.column_stack([E, s]) if self.ppt else E[:, None]
        er = y > 0
        self.clf = LogisticRegression(C=1.0).fit(Xc, er) if 0 < er.sum() < len(er) else None
        self.p_const = er.mean()
        pooled = np.polyfit(E[er], y[er], 1)
        if self.ppt:
            self.reg = {k: (np.polyfit(E[er & (s == k)], y[er & (s == k)], 1) if (er & (s == k)).sum() >= 3 else pooled)
                        for k in (0.0, 1.0)}
        else:
            self.reg = {0.0: pooled, 1.0: pooled}
        self.acc_mean = float(y[~er].mean()) if (~er).any() else 0.0
        return self

    def proba(self, df):
        E = df[self.e].to_numpy(float)
        s = (df["V_pre_total"].to_numpy() > self.v_eq).astype(float)
        Xc = np.column_stack([E, s]) if self.ppt else E[:, None]
        return self.clf.predict_proba(Xc)[:, 1] if self.clf is not None else np.full(len(df), self.p_const)

    def predict(self, df):
        E = df[self.e].to_numpy(float)
        s = (df["V_pre_total"].to_numpy() > self.v_eq).astype(float)
        ero = np.array([np.polyval(self.reg[k], e) for k, e in zip(s, E)])
        p = self.proba(df)
        if self.soft:
            return p * ero + (1 - p) * self.acc_mean
        return np.where(p >= 0.5, ero, self.acc_mean)


# ------------------------------------------------------------------ ShoreFor-flavoured
WS = 0.04  # m/s, sediment fall velocity for D50 ~ 0.35 mm [verify D50 at Truc Vert]; only rescales Omega


def shorefor_forcing(hydro: pd.DataFrame, events: pd.DataFrame, phi_days: float) -> pd.DataFrame:
    """ShoreFor-type forcing summed over each event interval (Davidson et al. 2013 form [verify]).

    Daily Omega = Hs / (ws Tp); Omega_eq(t) = weighted mean of past Omega over 2*phi days with
    weights 10^(-i/phi) (past only); F = P^0.5 (Omega_eq - Omega)/std(dOmega). Returns the sums of
    the erosive (F<0) and accretive (F>0) parts per event, sign-flipped so erosive forcing is > 0.
    """
    d = hydro[["hs", "tp"]].resample("1D").mean().interpolate()
    om = (d["hs"] / (WS * d["tp"])).to_numpy()
    P = (1025 * 9.81 ** 2 * d["hs"] ** 2 * d["tp"] / (64 * np.pi)).to_numpy()  # W/m
    n = int(2 * phi_days)
    w = 10 ** (-np.arange(1, n + 1) / phi_days)
    om_eq = np.full_like(om, np.nan)
    for t in range(1, len(om)):
        past = om[max(0, t - n):t][::-1]
        ww = w[:len(past)]
        om_eq[t] = np.sum(ww * past) / ww.sum()
    om_eq[0] = om[0]
    dom = om_eq - om
    F = np.sqrt(P) * dom / np.nanstd(dom)
    s = pd.Series(F, index=d.index)
    ero, acc = [], []
    for a, b in zip(events["survey_start"], events["survey_end"]):
        f = s[(s.index >= a) & (s.index < b)].to_numpy()
        ero.append(float(-f[f < 0].sum()))
        acc.append(float(f[f > 0].sum()))
    return pd.DataFrame({f"sf_ero_{phi_days:g}": ero, f"sf_acc_{phi_days:g}": acc}, index=events.index)


SF_PHIS = (15, 30, 60, 120, 240)


class ShoreForFlavour:
    """dV = a*F_ero + c*F_acc + b, phi chosen per training fold by in-sample RMSE."""
    name = "ShoreFor-flavoured (phi by train fit)"

    def fit(self, df, ctx):
        y = df[ctx.target].to_numpy(float)
        best = None
        for phi in SF_PHIS:
            X = _design(df, [f"sf_ero_{phi:g}", f"sf_acc_{phi:g}"])
            b, *_ = np.linalg.lstsq(X, y, rcond=None)
            r = np.sqrt(np.mean((X @ b - y) ** 2))
            if best is None or r < best[0]:
                best = (r, phi, b)
        _, self.phi, self.beta = best
        return self

    def predict(self, df):
        return _design(df, [f"sf_ero_{self.phi:g}", f"sf_acc_{self.phi:g}"]) @ self.beta


def baseline_models() -> dict:
    return {
        "clim": Climatology(),
        "clim_rate": ClimRate(),
        "evi_general": OLS([E_NB], "EVI General (dV ~ E_nbHAT)"),
        "ppt_all": PPTAllEvents(),
        "tpte_2stage": TwoStageThesis(ppt=False),
        "ppt_2stage": TwoStageThesis(ppt=True),
        "harley": OLS([E_ALL], "Harley-type (dV ~ sum Hs2 dt)"),
        "splinter": OLS([P_ALL, "n_clusters"], "Splinter-flavoured (dV ~ sum P dt + n_clusters)"),
        "eq_a": OLS([e_times_diseq], "Equilibrium A (dV ~ E(V-Veq))", state_fn=True),
        "eq_b": OLS([E_HAT, e_times_diseq], "Equilibrium B (dV ~ E + E(V-Veq))", state_fn=True),
        "shorefor": ShoreForFlavour(),
    }
