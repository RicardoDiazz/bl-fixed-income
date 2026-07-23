"""Pruebas unitarias para la clase GBMForecaster."""

import numpy as np
import pandas as pd
import pytest

from src.models.gbm import GBMForecaster


@pytest.fixture
def dummy_data():
    """Genera un dataset sintético para pruebas unitarias."""
    np.random.seed(42)
    dates = pd.date_range(start="2020-01-01", periods=50, freq="W")
    X = pd.DataFrame(
        {"feature_1": np.random.randn(50), "feature_2": np.random.randn(50)},
        index=dates,
    )

    y = pd.DataFrame(
        {"target_1": np.random.randn(50), "target_2": np.random.randn(50)}, index=dates
    )

    return X, y


def test_gbm_fit_predict(dummy_data):
    """Verifica el flujo fit/predict de GBMForecaster."""
    X, y = dummy_data

    X_train, X_test = X.iloc[:40], X.iloc[40:]
    y_train = y.iloc[:40]

    forecaster = GBMForecaster()
    forecaster.fit(X_train, y_train)

    preds = forecaster.predict(X_test)

    assert isinstance(preds, pd.DataFrame)
    assert preds.shape == (10, 2)
    assert list(preds.columns) == list(y.columns)
    assert not preds.isna().any().any()
