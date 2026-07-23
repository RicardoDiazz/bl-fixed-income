"""
Pruebas unitarias para el módulo de portafolios Baseline (B1, B2, B3, B3+).
"""

import pandas as pd
import pytest

from src.portfolio.baselines import compute_baseline_portfolios


@pytest.fixture
def mock_baseline_inputs():
    assets = ["SHY", "IEF", "TLT"]
    mu_bl = pd.Series([0.02, 0.035, 0.05], index=assets)
    historical_returns = pd.DataFrame(
        {
            "SHY": [0.001, -0.001, 0.002],
            "IEF": [0.002, -0.002, 0.003],
            "TLT": [0.003, -0.003, 0.004],
        },
        index=pd.date_range("2026-01-01", periods=3),
    )
    return mu_bl, historical_returns


def test_compute_baseline_portfolios(mock_baseline_inputs):
    mu_bl, historical_returns = mock_baseline_inputs
    baselines_df = compute_baseline_portfolios(mu_bl, historical_returns)

    assert isinstance(baselines_df, pd.DataFrame)
    # Verificamos que contenga los 4 baselines requeridos
    expected_columns = ["B1", "B2", "B3", "B3_plus"]
    for col in expected_columns:
        assert col in baselines_df.columns
