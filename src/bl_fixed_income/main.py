import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bl_fixed_income.data_loader import download_fixed_income_data
from bl_fixed_income.analytics import calculate_covariance_matrix, calculate_implied_equilibrium_returns, black_litterman_master_formula
from bl_fixed_income.allocator import maximize_sharpe_ratio

def plot_portfolio_comparison(assets, weights_eq, weights_bl):
    """Genera y guarda un grafico de barras comparativo de los pesos."""
    x = np.arange(len(assets))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))
    
    # Graficar barras de ambos portafolios
    rects1 = ax.bar(x - width/2, weights_eq.values * 100, width, label='Equilibrio de Mercado', color='#4A90E2')
    rects2 = ax.bar(x + width/2, weights_bl.values * 100, width, label='Black-Litterman Ajustado', color='#50E3C2')

    # Añadir etiquetas, titulos y detalles visuales profesionales
    ax.set_ylabel('Asignación de Pesos (%)', fontsize=12)
    ax.set_title('Comparativa de Portafolios: Mercado vs. Black-Litterman', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(assets, fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Añadir los valores numericos encima de las barras
    ax.bar_label(rects1, padding=3, fmt='%.1f%%')
    ax.bar_label(rects2, padding=3, fmt='%.1f%%')

    fig.tight_layout()
    
    # Guardar como imagen PNG de alta definicion
    output_path = "portfolio_comparison.png"
    plt.savefig(output_path, dpi=300)
    print(f"\n[Grafico guardado con exito en: {output_path}]")
    plt.close()

def run_pipeline():
    print("==========================================================")
    print("   EJECUTANDO PIPELINE: OPTIMIZACION Y VISUALIZACION")
    print("==========================================================\n")
    
    assets = ["SHY", "IEF", "TLT"]
    prices, returns = download_fixed_income_data(tickers=assets, period="5y")
    
    cov_matrix = calculate_covariance_matrix(returns)
    market_weights = [1/3, 1/3, 1/3]
    
    pi = calculate_implied_equilibrium_returns(market_weights, cov_matrix)
    
    # Vista optimista en TLT (Largo Plazo)
    P = [[0, 0, 1]] 
    Q = [0.05]      
    Omega = [[0.00001]] 
    
    mu_bl, cov_bl = black_litterman_master_formula(pi, cov_matrix, P, Q, Omega)
    
    print("\nOptimizando portafolios...")
    weights_eq = maximize_sharpe_ratio(pi, cov_matrix, risk_free_rate=0.035)
    weights_bl = maximize_sharpe_ratio(mu_bl, cov_bl, risk_free_rate=0.035)
    
    # Invocar la generacion del grafico
    plot_portfolio_comparison(assets, weights_eq, weights_bl)

if __name__ == "__main__":
    run_pipeline()
