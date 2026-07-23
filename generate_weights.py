"""
Script para cargar los rendimientos esperados posteriores (mu_bl.parquet),
ejecutar la optimización de media-varianza y guardar las ponderaciones óptimas.
"""

import pandas as pd

from src.bl.optimize import optimize_portfolio_mean_variance

# 1. Cargar mu_bl desde el archivo parquet
mu_bl_df = pd.read_parquet("mu_bl.parquet")
mu_bl = mu_bl_df["mu_bl"]

# 2. Definir la matriz de covarianza (alineada con los activos de mu_bl)
assets = mu_bl.index.tolist()
sigma = pd.DataFrame(
    [[0.001, 0.0005, 0.0002], [0.0005, 0.002, 0.001], [0.0002, 0.001, 0.004]],
    index=assets,
    columns=assets,
)

# 3. Ejecutar la optimización de media-varianza (delta = 2.5)
weights = optimize_portfolio_mean_variance(mu_bl, sigma, risk_aversion=2.5)

# 4. Guardar las ponderaciones óptimas en parquet
df_weights = weights.to_frame()
df_weights.to_parquet("optimal_weights.parquet")

print("--- Ponderaciones Óptimas del Portafolio Black-Litterman ---")
print(weights)
print("\n¡Archivo optimal_weights.parquet guardado con éxito!")
