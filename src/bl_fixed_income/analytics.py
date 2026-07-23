import numpy as np
import pandas as pd


def calculate_covariance_matrix(returns, periods_per_year=252):
    """Calcula la matriz de covarianza anualizada de los rendimientos de los bonos."""
    daily_cov = returns.cov()
    annualized_cov = daily_cov * periods_per_year
    return annualized_cov


def calculate_implied_equilibrium_returns(weights, cov_matrix, risk_aversion=2.5):
    """Calcula los rendimientos implicitos de equilibrio del mercado."""
    w = np.array(weights).reshape(-1, 1)
    sigma = cov_matrix.values
    implied_returns = risk_aversion * np.dot(sigma, w)
    return pd.Series(implied_returns.flatten(), index=cov_matrix.index)


def black_litterman_master_formula(pi, sigma, P, Q, Omega, tau=0.05):
    """
    Implementa la formula maestra de Black-Litterman para calcular los rendimientos
    esperados ajustados (mu) y la nueva matriz de covarianza.
    """
    # Convertir todo a arreglos de numpy y asegurar dimensiones de vectores columna
    pi_vec = np.array(pi).reshape(-1, 1)
    Q_vec = np.array(Q).reshape(-1, 1)
    P_mat = np.array(P)
    Omega_mat = np.array(Omega)
    sigma_mat = np.array(sigma)

    # 1. Calcular el primer componente: Inversa de (tau * Sigma)
    scaled_sigma_inv = np.linalg.inv(tau * sigma_mat)

    # 2. Calcular el componente de las vistas: P^T * Omega^-1 * P
    omega_inv = np.linalg.inv(Omega_mat)
    views_component = np.dot(np.dot(P_mat.T, omega_inv), P_mat)

    # 3. Matriz de informacion total (Inversa del denominador general)
    total_info_inv = np.linalg.inv(scaled_sigma_inv + views_component)

    # 4. Calcular el vector de rendimientos ajustados (mu)
    rhs = np.dot(scaled_sigma_inv, pi_vec) + np.dot(np.dot(P_mat.T, omega_inv), Q_vec)
    mu_bl = np.dot(total_info_inv, rhs)

    # 5. Calcular la nueva matriz de covarianza ajustada
    sigma_bl = sigma_mat + total_info_inv

    # Convertir los resultados de vuelta a formatos limpios de Pandas
    mu_series = pd.Series(mu_bl.flatten(), index=pi.index)
    sigma_df = pd.DataFrame(sigma_bl, index=sigma.index, columns=sigma.columns)

    return mu_series, sigma_df


if __name__ == "__main__":
    print("Probando modulo de analitica completo con Black-Litterman...")
    assets = ["SHY", "IEF", "TLT"]
    np.random.seed(42)
    simulated_returns = pd.DataFrame(
        np.random.normal(0, 0.001, (100, 3)), columns=assets
    )

    cov = calculate_covariance_matrix(simulated_returns)
    equal_weights = [1 / 3, 1 / 3, 1 / 3]
    pi = calculate_implied_equilibrium_returns(equal_weights, cov)

    # Supongamos una vista: "TLT (Largo plazo) rendira un 2% anualizado absoluto"
    # P: [[0, 0, 1]] (Afecta solo al tercer activo)
    # Q: [0.02]
    # Omega: [[0.0001]] (Confianza alta)
    P = [[0, 0, 1]]
    Q = [0.02]
    Omega = [[0.0001]]

    mu_bl, cov_bl = black_litterman_master_formula(pi, cov, P, Q, Omega)
    print("\n--- Rendimientos Originales de Equilibrio (Pi) ---")
    print(pi)
    print("\n--- Rendimientos Ajustados por Black-Litterman (Mu BL) ---")
    print(mu_bl)
