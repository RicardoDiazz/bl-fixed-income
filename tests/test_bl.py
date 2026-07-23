"""
Pruebas unitarias para el ensamblaje Black-Litterman (Prior, Omega y Posterior).
"""

import numpy as np
import pandas as pd
import pytest

from src.bl.omega import calculate_omega_diagonal
from src.bl.posterior import calculate_black_litterman_posterior
from src.bl.prior import calculate_implied_equilibrium_returns


@pytest.fixture
def mock_market_data():
    assets = ["SHY", "IEF", "TLT"]
    sigma = pd.DataFrame(
        [[0.001, 0.0005, 0.0002], [0.0005, 0.002, 0.001], [0.0002, 0.001, 0.004]],
        index=assets,
        columns=assets,
    )
    weights = pd.Series([0.5, 0.3, 0.2], index=assets)
    return sigma, weights


def test_calculate_implied_equilibrium_returns(mock_market_data):
    sigma, weights = mock_market_data
    delta = 2.5
    pi = calculate_implied_equilibrium_returns(delta, sigma, weights)

    assert isinstance(pi, pd.Series)
    assert len(pi) == 3
    assert pi.name == "implied_returns"


def test_calculate_omega_diagonal(mock_market_data):
    sigma, _ = mock_market_data
    p_matrix = np.array([[1, -1, 0], [0, 1, -1]])
    omega = calculate_omega_diagonal(p_matrix, sigma, tau=0.05)

    assert isinstance(omega, np.ndarray)
    assert omega.shape == (2, 2)
    assert np.all(np.diagonal(omega) > 0)


def test_calculate_black_litterman_posterior(mock_market_data):
    sigma, weights = mock_market_data
    delta = 2.5
    pi = calculate_implied_equilibrium_returns(delta, sigma, weights)

    p_matrix = np.array([[1, -1, 0]])
    q_vector = np.array([0.01])
    omega = calculate_omega_diagonal(p_matrix, sigma, tau=0.05)

    mu_bl = calculate_black_litterman_posterior(
        sigma, pi, p_matrix, q_vector, omega, tau=0.05
    )

    assert isinstance(mu_bl, pd.Series)
    assert len(mu_bl) == 3
    assert mu_bl.name == "mu_bl"
