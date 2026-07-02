import numpy as np
import pandas as pd
from scipy.optimize import minimize

def maximize_sharpe_ratio(expected_returns, cov_matrix, risk_free_rate=0.03):
    """
    Encuentra los pesos optimos que maximizan el Ratio de Sharpe.
    Minimiza el negativo del Ratio de Sharpe.
    """
    num_assets = len(expected_returns)
    returns = expected_returns.values
    sigma = cov_matrix.values
    
    # 1. Definir la funcion objetivo (Negativo del Ratio de Sharpe)
    def objective(weights):
        port_return = np.dot(weights, returns)
        port_volatility = np.sqrt(np.dot(weights.T, np.dot(sigma, weights)))
        sharpe = (port_return - risk_free_rate) / port_volatility if port_volatility > 0 else 0
        return -sharpe

    # 2. Restricciones: La suma de los pesos debe ser igual a 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0})
    
    # 3. Limites: Pesos entre 0 y 1 (No se permiten ventas en corto)
    bounds = tuple((0.0, 1.0) for _ in range(num_assets))
    
    # 4. Asignacion inicial equitativa
    init_weights = num_assets * [1.0 / num_assets]
    
    # 5. Ejecutar la optimizacion numerica
    result = minimize(objective, init_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    
    if not result.success:
        raise BaseException("La optimizacion de portafolio no convergio: " + result.message)
        
    return pd.Series(result.x, index=expected_returns.index)
