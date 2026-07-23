"""Pruebas unitarias para la clase TransformerForecaster."""

import numpy as np
import pandas as pd
import pytest

from src.models.transformer import TransformerForecaster


@pytest.fixture
def dummy_data():
    """Genera un dataset sintético para pruebas unitarias de PyTorch Transformer."""
    np.random.seed(42)
    dates = pd.date_range(start="2020-01-01", periods=30, freq="W")
    X = pd.DataFrame(
        {"feature_1": np.random.randn(30), "feature_2": np.random.randn(30)},
        index=dates,
    )

    y = pd.DataFrame(
        {"target_1": np.random.randn(30), "target_2": np.random.randn(30)}, index=dates
    )

    return X, y


def test_transformer_fit_predict(dummy_data):
    """Verifica el flujo fit/predict de TransformerForecaster."""
    X, y = dummy_data
    seq_len = 4

    X_train, y_train = X.iloc[:20], y.iloc[:20]
    X_test_seq = X.iloc[16:20]  # Ventana de tamaño seq_len=4

    forecaster = TransformerForecaster(seq_len=seq_len, epochs=5, batch_size=8)
    forecaster.fit(X_train, y_train)

    preds = forecaster.predict(X_test_seq)

    assert isinstance(preds, pd.DataFrame)
    assert preds.shape == (1, 2)
    assert list(preds.columns) == list(y.columns)
    assert not preds.isna().any().any()
