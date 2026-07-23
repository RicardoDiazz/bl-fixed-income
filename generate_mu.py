import numpy as np
import pandas as pd

from src.bl.omega import calculate_omega_diagonal
from src.bl.posterior import calculate_black_litterman_posterior
from src.bl.prior import calculate_implied_equilibrium_returns

# Definir datos base de prueba para generar el entregable
assets = ["SHY", "IEF", "TLT"]
sigma = pd.DataFrame(
    [[0.001, 0.0005, 0.0002], [0.0005, 0.002, 0.001], [0.0002, 0.001, 0.004]],
    index=assets,
    columns=assets,
)
weights = pd.Series([0.5, 0.3, 0.2], index=assets)
delta = 2.5

# Calcular equilibrio y posterior
pi = calculate_implied_equilibrium_returns(delta, sigma, weights)
p_matrix = np.array([[1, -1, 0]])
q_vector = np.array([0.01])
omega = calculate_omega_diagonal(p_matrix, sigma, tau=0.05)

mu_bl = calculate_black_litterman_posterior(
    sigma, pi, p_matrix, q_vector, omega, tau=0.05
)

# Guardar en parquet como se solicita en los entregables
df_output = mu_bl.to_frame()
df_output.to_parquet("mu_bl.parquet")
print("¡Archivo mu_bl.parquet generado con éxito!")
