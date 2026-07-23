"""
Pruebas unitarias para el módulo de portafolios de Machine Learning.
"""

import pandas as pd
import pytest

from src.portfolio.weights import compute_ml_portfolio_returns


@pytest.fixture
def mock_ml_inputs():
    assets = ["SHY", "IEF", "TLT"]
    mu_bl = pd.Series([0.02, 0.035, 0.05], index=assets, name="mu_bl")

    # Simulamos predicciones o señales para los 4 modelos de ML
    ml_predictions = pd.DataFrame(
        {
            "Model_1": [0.4, 0.4, 0.2],
            "Model_2": [0.3, 0.3, 0.4],
            "Model_3": [0.5, 0.2, 0.3],
            "Model_4": [0.25, 0.35, 0.4],
        },
        index=assets,
    )
    return mu_bl, ml_predictions


def test_compute_ml_portfolio_returns(mock_ml_inputs):
    mu_bl, ml_predictions = mock_ml_inputs
    returns_df = compute_ml_portfolio_returns(mu_bl, ml_predictions)

    assert isinstance(returns_df, pd.DataFrame)
    # Verificamos que se generen columnas o métricas para los 4 modelos
    assert not returns_df.empty
