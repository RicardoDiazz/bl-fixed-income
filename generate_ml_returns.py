"""
Script de ejecución para calcular y exportar los retornos
de los portafolios de Machine Learning (Semana 11).
"""

import pandas as pd

from src.portfolio.weights import compute_ml_portfolio_returns


def main():
    # Cargamos el mu_bl generado en la semana 10
    mu_bl = pd.read_parquet("mu_bl.parquet").squeeze("columns")

    # Simulamos o cargamos las predicciones de los 4 modelos de ML
    # (ajustable según los archivos de modelos que manejen en el equipo)
    ml_predictions = pd.DataFrame(
        {
            "Model_1": [0.4, 0.4, 0.2],
            "Model_2": [0.3, 0.3, 0.4],
            "Model_3": [0.5, 0.2, 0.3],
            "Model_4": [0.25, 0.35, 0.4],
        },
        index=mu_bl.index,
    )

    # Computamos los portafolios ML
    returns_df = compute_ml_portfolio_returns(mu_bl, ml_predictions)

    # Guardamos el entregable requerido en formato parquet
    returns_df.to_parquet("returns_ml.parquet")
    print("¡Archivo returns_ml.parquet generado exitosamente!")


if __name__ == "__main__":
    main()
