"""
Módulo para el cálculo del rendimiento posterior ajustado de Black-Litterman (Mu_BL).
Black-Litterman Posterior Module.
"""

import numpy as np
import pandas as pd


def calculate_black_litterman_posterior(
    sigma: pd.DataFrame,
    pi: pd.Series,
    p_matrix: np.ndarray,
    q_vector: np.ndarray,
    omega: np.ndarray,
    tau: float = 0.05,
) -> pd.Series:
    """Calcula el vector de rendimientos esperados combinados (mu_BL)

    utilizando la formulación analítica de Black-Litterman.
    """
    sigma_mat = sigma.values
    pi_vec = pi.values.reshape(-1, 1)
    q_vec = q_vector.reshape(-1, 1)

    # Inversa de la matriz de covarianza escalada (tau * Sigma)
    inv_tau_sigma = np.linalg.inv(tau * sigma_mat)

    # Inversa de la matriz de incertidumbre de las vistas (Omega)
    inv_omega = np.linalg.inv(omega)

    # Término de precisión del mercado y de las vistas
    # M_inv = ( (tau*Sigma)^-1 + P' * Omega^-1 * P )^-1
    middle_matrix = inv_tau_sigma + np.dot(p_matrix.T, np.dot(inv_omega, p_matrix))
    inv_middle = np.linalg.inv(middle_matrix)

    # Componentes del vector posterior
    term_pi = np.dot(inv_tau_sigma, pi_vec)
    term_q = np.dot(p_matrix.T, np.dot(inv_omega, q_vec))

    # mu_BL = M_inv @ ( (tau*Sigma)^-1 * Pi + P' * Omega^-1 * Q )
    mu_bl_vec = np.dot(inv_middle, term_pi + term_q)

    return pd.Series(mu_bl_vec.flatten(), index=sigma.index, name="mu_bl")
