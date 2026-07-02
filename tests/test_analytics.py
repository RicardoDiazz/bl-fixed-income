import pytest
import numpy as np
import pandas as pd
from bl_fixed_income.analytics import calculate_covariance_matrix, calculate_implied_equilibrium_returns, black_litterman_master_formula

def test_black_litterman_no_views_collapses_to_equilibrium():
    """
    Verifica matematicamente que si las matrices de vistas estan vacias o
    la incertidumbre tiende a infinito, el modelo regresa al equilibrio de mercado.
    """
    assets = ["SHY", "IEF", "TLT"]
    np.random.seed(123)
    simulated_returns = pd.DataFrame(np.random.normal(0, 0.001, (100, 3)), columns=assets)
    
    cov = calculate_covariance_matrix(simulated_returns)
    market_weights = [1/3, 1/3, 1/3]
    pi = calculate_implied_equilibrium_returns(market_weights, cov)
    
    # Configuramos una vista con una incertidumbre (Omega) gigantesca (baja confianza)
    # Lo que equivale analiticamente a no tener vistas significativas.
    P = [[0, 0, 1]]
    Q = [0.10] # Una opinion exagerada del 10%
    Omega = [[1e10]] # Certidumbre casi nula (varianza infinita)
    
    mu_bl, _ = black_litterman_master_formula(pi, cov, P, Q, Omega, tau=0.05)
    
    # Comprobar que los rendimientos ajustados son casi identicos a Pi (Equilibrio)
    # Tolerancia de diferencias infinitesimales debido a precision flotante
    np.testing.assert_allclose(mu_bl.values, pi.values, rtol=1e-4, atol=1e-4)
