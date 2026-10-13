"""Small-n ML models: LightGBM, XGBoost, random forest, GP, two-stage and hybrid residual.

With n ~ 50 events every model is deliberately heavily regularised (depth-2 trees, few
leaves, large min_child_samples, shrinkage). Hyper-parameters are FIXED a priori (no tuning
on the test folds). Seeds fixed to protocol.SEED.
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

from .baselines import E_HAT, OLS, e_times_diseq
from .protocol import SEED

FEATURES = [
    "E_Hs2dt_stormHAT_m2h", "E_Pflux_storm_GJ_m", "peak_hs", "hat_exceed_hours_storm",
    "n_clusters", "dsls", "interval_days", "season_code", "V_anom_past", "berm_volume_pre",
    "intertidal_slope_pre",
]
GP_FEATURES = ["E_Hs2dt_stormHAT_m2h", "V_anom_past", "berm_volume_pre", "interval_days"]

LGB_PARAMS = dict(n_estimators=300, learning_rate=0.03, num_leaves=4, max_depth=2, min_child_samples=6,
                  subsample=0.8, subsample_freq=1, colsample_bytree=0.8, reg_lambda=2.0,
                  random_state=SEED, verbose=-1, deterministic=True, force_row_wise=True)
XGB_PARAMS = dict(n_estimators=300, learning_rate=0.03, max_depth=2, min_child_weight=6, subsample=0.8,
                  colsample_bytree=0.8, reg_lambda=2.0, random_state=SEED, n_jobs=1)
RF_PARAMS = dict(n_estimators=500, max_depth=3, min_samples_leaf=4, max_features=0.5, random_state=SEED, n_jobs=1)


class Tree:
    def __init__(self, kind="lgbm", features=FEATURES, name=None, objective=None, alpha=None):
        self.kind, self.features = kind, list(features)
        self.objective, self.alpha = objective, alpha
        self.name = name or {"lgbm": "LightGBM", "xgb": "XGBoost", "rf": "Random forest"}[kind]

    def _make(self):
        if self.kind == "lgbm":
            import lightgbm as lgb
            kw = dict(LGB_PARAMS)
            if self.objective:
                kw.update(objective=self.objective, alpha=self.alpha)
            return lgb.LGBMRegressor(**kw)
        if self.kind == "xgb":
            import xgboost as xgb
            return xgb.XGBRegressor(**XGB_PARAMS)
        from sklearn.ensemble import RandomForestRegressor
        return RandomForestRegressor(**RF_PARAMS)

    def fit(self, df, ctx):
        self.m = self._make()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.m.fit(df[self.features].astype(float), df[ctx.target].to_numpy(float))
        return self

    def predict(self, df):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return np.asarray(self.m.predict(df[self.features].astype(float)), float)


class GP:
    """GP regression, ConstantKernel*RBF(ARD) + White on standardised inputs, normalize_y.
    energy enters as log1p (heavy right tail)."""
    name = "Gaussian process (RBF-ARD + White)"

    def __init__(self, features=GP_FEATURES):
        self.features = list(features)

    def _X(self, df):
        X = df[self.features].astype(float).copy()
        for c in X.columns:
            if c.startswith("E_"):
                X[c] = np.log1p(X[c])
        return X.to_numpy()

    def fit(self, df, ctx):
        from sklearn.gaussian_process import GaussianProcessRegressor
        from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
        from sklearn.preprocessing import StandardScaler
        X = self._X(df)
        self.sc = StandardScaler().fit(X)
        k = ConstantKernel(1.0, (1e-2, 1e2)) * RBF(np.ones(X.shape[1]), (1e-1, 1e2)) + WhiteKernel(0.5, (1e-3, 1e1))
        self.m = GaussianProcessRegressor(k, normalize_y=True, n_restarts_optimizer=5, random_state=SEED)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.m.fit(self.sc.transform(X), df[ctx.target].to_numpy(float))
        return self

    def predict(self, df, return_std=False):
        mu, sd = self.m.predict(self.sc.transform(self._X(df)), return_std=True)
        return (mu, sd) if return_std else mu


class TwoStageML:
    """Classifier (logistic on standardised E_HAT, V_anom_past, berm) -> P(erode); regressors
    per branch (OLS on E_HAT within training events of that sign). Prediction = expected value
    p*mu_ero + (1-p)*mu_acc. Branch fitting uses TRAINING labels only (never test dV)."""
    name = "Two-stage (logit -> OLS per branch, expected value)"
    cls_feats = ["E_Hs2dt_stormHAT_m2h", "V_anom_past", "berm_volume_pre"]

    def fit(self, df, ctx):
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        y = df[ctx.target].to_numpy(float)
        er = y > 0
        self.clf = make_pipeline(StandardScaler(), LogisticRegression(C=1.0)).fit(df[self.cls_feats].astype(float), er)
        E = df[E_HAT].to_numpy(float)
        self.r_ero = np.polyfit(E[er], y[er], 1)
        self.r_acc = np.polyfit(E[~er], y[~er], 1) if (~er).sum() >= 3 else np.array([0.0, y[~er].mean()])
        return self

    def proba(self, df):
        return self.clf.predict_proba(df[self.cls_feats].astype(float))[:, 1]

    def predict(self, df):
        p = self.proba(df)
        E = df[E_HAT].to_numpy(float)
        return p * np.polyval(self.r_ero, E) + (1 - p) * np.polyval(self.r_acc, E)


class HybridResidual:
    """Equilibrium-B baseline + shallow LightGBM on its in-sample residuals (shrunk: 100 trees)."""
    name = "Hybrid (Equilibrium B + LightGBM residual)"

    def __init__(self, features=FEATURES):
        self.features = list(features)

    def fit(self, df, ctx):
        import lightgbm as lgb
        self.base = OLS([E_HAT, e_times_diseq], "eq_b", state_fn=True).fit(df, ctx)
        r = df[ctx.target].to_numpy(float) - self.base.predict(df)
        kw = dict(LGB_PARAMS, n_estimators=100)
        self.m = lgb.LGBMRegressor(**kw).fit(df[self.features].astype(float), r)
        return self

    def predict(self, df):
        return self.base.predict(df) + self.m.predict(df[self.features].astype(float))


def ml_models(features=FEATURES) -> dict:
    return {
        "lgbm": Tree("lgbm", features),
        "xgb": Tree("xgb", features),
        "rf": Tree("rf", features),
        "gp": GP(),
        "two_stage_ml": TwoStageML(),
        "hybrid": HybridResidual(features),
    }
