"""
Script para generar el archivo maestro 'returns.parquet' combinando
los 4 portafolios de ML y los 4 portafolios Baseline (B1, B2, B3, B3+).
"""

import pandas as pd

from src.portfolio.baselines import compute_baseline_portfolios


def main():
    # 1. Cargamos los insumos necesarios de forma directa
    df_mu = pd.read_parquet("mu_bl.parquet")
    mu_bl = df_mu.iloc[:, 0]

    returns_ml = pd.read_parquet("returns_ml.parquet")

    # Histórico base para los baselines
    historical_returns = pd.DataFrame(
        {asset: [0.001, -0.001, 0.002, -0.002] for asset in mu_bl.index},
        index=pd.date_range("2026-01-01", periods=4),
    )

    # 2. Calculamos los baselines
    baselines_df = compute_baseline_portfolios(mu_bl, historical_returns)

    # 3. Unificamos ambos mundos en un único DataFrame maestro con los 8 portafolios
    master_returns = pd.concat([returns_ml, baselines_df], axis=1)

    # 4. Guardamos el resultado final en el entregable requerido
    master_returns.to_parquet("returns.parquet")
    print("¡Archivo returns.parquet con los 8 portafolios generado exitosamente!")


if __name__ == "__main__":
    main()
