"""
Módulo para construir los 4 portafolios de referencia
(Baselines: B1, B2, B3, B3+).
"""

import pandas as pd


def compute_baseline_portfolios(
    mu_bl: pd.Series, historical_returns: pd.DataFrame
) -> pd.DataFrame:
    """Calcula los retornos de los 4 portafolios baseline:

    - B1: Igual ponderación (Naive Diversification / 1/N)
    - B2: Minimizacion de Varianza / Paridad de Riesgo básica
    - B3: Benchmark de Mercado / Ponderación por capitalización
    - B3+: Baseline ajustado con restricciones tácticas
    """
    assets = mu_bl.index
    n = len(assets)

    # B1: Pesos equitativos (1/N)
    w_b1 = pd.Series(1.0 / n, index=assets)

    # B2: Simulación de mínima varianza (o ponderación inversa a volatilidad)
    vol = historical_returns.std()
    w_b2 = (1.0 / vol) / (1.0 / vol).sum()

    # B3: Ponderación de mercado simulada o uniforme base
    w_b3 = pd.Series(1.0 / n, index=assets)  # Ajustable según pesos de mercado reales

    # B3+: Versión avanzada con sesgo hacia los retornos esperados de Black-Litterman
    w_b3_plus = mu_bl / mu_bl.sum()

    # Calculamos retornos esperados o ponderados para cada baseline
    baselines_df = pd.DataFrame(
        {
            "B1": w_b1.dot(mu_bl),
            "B2": w_b2.dot(mu_bl),
            "B3": w_b3.dot(mu_bl),
            "B3_plus": w_b3_plus.dot(mu_bl),
        },
        index=["Expected_Return"],
    )
    return baselines_df
