"""
Módulo de optimización de portafolios de Media-Varianza utilizando los
rendimientos posteriores de Black-Litterman (Mu_BL).
"""

import numpy as np
import pandas as pd


def optimize_portfolio_mean_variance(
    mu: pd.Series, sigma: pd.DataFrame, risk_aversion: float = 2.5
) -> pd.Series:
    """Calcula las ponderaciones óptimas del portafolio maximizando

    la utilidad esperada de media-varianza con la restricción
    de que los pesos sumen 1.
    """
    mu_vec = mu.reindex(sigma.index).values
    sigma_inv = np.linalg.inv(sigma.values)

    # Solución analítica para pesos sin restricciones de no-negatividad:
    # w = (1 / delta) * Sigma^-1 * mu + ... (con la restricción de suma 1)
    # Aplicamos la fórmula cerrada clásica del portafolio óptimo mean-variance:
    ones = np.ones(len(mu_vec))

    # W_unconstrained = (1 / delta) * Sigma^-1 @ mu
    # Normalizado para que sumen 1 incorporando la restricción de presupuesto
    inv_sigma_ones = np.dot(sigma_inv, ones)
    inv_sigma_mu = np.dot(sigma_inv, mu_vec)

    A = np.dot(ones.T, inv_sigma_ones)
    B = np.dot(ones.T, inv_sigma_mu)

    # Multiplicador de Lagrange y solución analítica con suma de pesos = 1
    # w = (Sigma^-1 * mu) / delta + lambda * (Sigma^-1 * 1)
    lambda_param = (1.0 - B / risk_aversion) / A

    optimal_weights = (inv_sigma_mu / risk_aversion) + (lambda_param * inv_sigma_ones)

    return pd.Series(optimal_weights, index=sigma.index, name="optimal_weights")
