"""
Módulo para el cálculo de la matriz de incertidumbre de las vistas (Omega).
Black-Litterman Uncertainty of Views Module.
"""

import numpy as np
import pandas as pd


def calculate_omega_diagonal(
    p_matrix: np.ndarray, sigma: pd.DataFrame, tau: float = 0.05
) -> np.ndarray:
    """Calcula la matriz Omega utilizando una aproximación diagonal proporcional

    basada en la incertidumbre del prior (tau * P * Sigma * P').
    """
    sigma_mat = sigma.values
    # Varianzas escaladas de las vistas proyectadas
    omega_variance = tau * np.diag(np.dot(p_matrix, np.dot(sigma_mat, p_matrix.T)))
    return np.diag(omega_variance)
