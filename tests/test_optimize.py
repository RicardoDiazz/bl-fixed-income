"""
Pruebas unitarias para el módulo de optimización de portafolios.
"""

import numpy as np
import pandas as pd
import pytest

from src.bl.optimize import optimize_portfolio_mean_variance


@pytest.fixture
def mock_optimization_inputs():
    assets = ["SHY", "IEF", "TLT"]
    sigma = pd.DataFrame(
        [[0.001, 0.0005, 0.0002], [0.0005, 0.002, 0.001], [0.0002, 0.001, 0.004]],
        index=assets,
        columns=assets,
    )
    mu_bl = pd.Series([0.02, 0.035, 0.05], index=assets, name="mu_bl")
    return mu_bl, sigma


def test_optimize_portfolio_mean_variance(mock_optimization_inputs):
    mu_bl, sigma = mock_optimization_inputs
    weights = optimize_portfolio_mean_variance(mu_bl, sigma, risk_aversion=2.5)

    assert isinstance(weights, pd.Series)
    assert len(weights) == 3
    # Verificar que los pesos sumen 1 (restricción de presupuesto)
    assert np.isclose(weights.sum(), 1.0, atol=1e-5)
    assert weights.name == "optimal_weights"
