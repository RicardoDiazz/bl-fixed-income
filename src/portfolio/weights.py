"""
Módulo para construir los portafolios de Machine Learning utilizando
los retornos esperados de Black-Litterman (mu_BL).
"""

import pandas as pd


def compute_ml_portfolio_returns(
    mu_bl: pd.Series, ml_predictions_df: pd.DataFrame
) -> pd.DataFrame:
    """Calcula los retornos y ponderaciones de los 4 portafolios

    combinando las señales de los modelos con los retornos
    posteriores de Black-Litterman.
    """
    # Normalizamos los pesos/señales de cada modelo
    weights_df = ml_predictions_df.div(ml_predictions_df.sum(axis=0), axis=1)

    # Calculamos el retorno esperado del portafolios para cada modelo
    portfolio_returns = weights_df.T.dot(mu_bl)

    # Devolvemos un DataFrame estructurado con los resultados por modelo
    result_df = pd.DataFrame(
        {
            "Weights": weights_df.to_dict(orient="list"),
            "Expected_Return": portfolio_returns,
        }
    )
    return result_df
