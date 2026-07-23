"""Módulo para el modelo baseline GBM (LightGBM) en Fixed Income."""

from typing import Dict, Optional

import lightgbm as lgb
import pandas as pd


class GBMForecaster:
    """Encapsula el entrenamiento y predicción de modelos GBM para cada target."""

    def __init__(self, params: Optional[Dict] = None):
        """Inicializa los hiperparámetros de LightGBM."""
        self.default_params = {
            "objective": "regression",
            "metric": "rmse",
            "boosting_type": "gbdt",
            "n_estimators": 100,
            "learning_rate": 0.05,
            "num_leaves": 31,
            "random_state": 42,
            "verbose": -1,
            "n_jobs": -1,
        }
        if params:
            self.default_params.update(params)

        self.models: Dict[str, lgb.LGBMRegressor] = {}

    def fit(self, X: pd.DataFrame, y: pd.DataFrame) -> "GBMForecaster":
        """Entrena un modelo LightGBM individual por cada columna target."""
        for col in y.columns:
            model = lgb.LGBMRegressor(**self.default_params)
            model.fit(X, y[col])
            self.models[col] = model
        return self

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """Genera predicciones para todos los targets."""
        predictions = {}
        for col, model in self.models.items():
            predictions[col] = model.predict(X)
        return pd.DataFrame(predictions, index=X.index)
