import numpy as np
import pandas as pd

def calculate_covariance_matrix(returns, periods_per_year=252):
    """
    Calcula la matriz de covarianza anualizada de los rendimientos de los bonos.
    """
    daily_cov = returns.cov()
    annualized_cov = daily_cov * periods_per_year
    return annualized_cov

def calculate_implied_equilibrium_returns(weights, cov_matrix, risk_aversion=2.5):
    """
    Calcula los rendimientos implicitos de equilibrio del mercado (Reversa de Optimizacion).
    Pi = lambda * Sigma * w
    """
    w = np.array(weights).reshape(-1, 1)
    sigma = cov_matrix.values
    implied_returns = risk_aversion * np.dot(sigma, w)
    return pd.Series(implied_returns.flatten(), index=cov_matrix.index)

if __name__ == "__main__":
    print("Probando modulo de analitica...")
    assets = ["SHY", "IEF", "TLT"]
    np.random.seed(42)
    simulated_returns = pd.DataFrame(np.random.normal(0, 0.001, (100, 3)), columns=assets)
    
    cov = calculate_covariance_matrix(simulated_returns)
    print("\n--- Matriz de Covarianza Anualizada (Simulada) ---")
    print(cov)
    
    equal_weights = [1/3, 1/3, 1/3]
    pi = calculate_implied_equilibrium_returns(equal_weights, cov)
    print("\n--- Rendimientos Implicitos de Equilibrio ---")
    print(pi)
