"""
Módulo para el cálculo del rendimiento de equilibrio del mercado (Pi).
Black-Litterman Prior Module.
"""

import numpy as np
import pandas as pd


def calculate_implied_equilibrium_returns(
    delta: float, sigma: pd.DataFrame, weights: pd.Series
) -> pd.Series:
    """Calcula el vector de rendimientos de equilibrio implícito (Pi).

    Formula: Pi = delta * (Sigma @ weights)
    """
    # Asegurar alineación de índices
    w = weights.reindex(sigma.index)
    pi_values = delta * np.dot(sigma.values, w.values)
    return pd.Series(pi_values, index=sigma.index, name="implied_returns")
