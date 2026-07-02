import tomllib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bl_fixed_income.data_loader import download_fixed_income_data
from bl_fixed_income.analytics import calculate_covariance_matrix, calculate_implied_equilibrium_returns, black_litterman_master_formula
from bl_fixed_income.allocator import maximize_sharpe_ratio

def load_settings():
    """Carga los parametros de configuracion desde el archivo settings.toml."""
    with open("settings.toml", "r", encoding="utf-8-sig") as f:
        return tomllib.loads(f.read())

def plot_portfolio_comparison(assets, weights_eq, weights_bl):
    """Genera y guarda un grafico de barras comparativo de los pesos."""
    x = np.arange(len(assets))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))
    rects1 = ax.bar(x - width/2, weights_eq.values * 100, width, label='Equilibrio de Mercado', color='#4A90E2')
    rects2 = ax.bar(x + width/2, weights_bl.values * 100, width, label='Black-Litterman Ajustado', color='#50E3C2')

    ax.set_ylabel('Asignación de Pesos (%)', fontsize=12)
    ax.set_title('Comparativa de Portafolios: Mercado vs. Black-Litterman', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(assets, fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    ax.bar_label(rects1, padding=3, fmt='%.1f%%')
    ax.bar_label(rects2, padding=3, fmt='%.1f%%')

    fig.tight_layout()
    output_path = "portfolio_comparison.png"
    plt.savefig(output_path, dpi=300)
    print(f"\n[Grafico guardado con exito en: {output_path}]")
    plt.close()

def run_pipeline():
    print("==========================================================")
    print("   EJECUTANDO PIPELINE: BLACK-LITTERMAN DINÁMICO")
    print("==========================================================\n")
    
    # 1. Cargar configuracion desde el archivo TOML externo
    config = load_settings()
    
    market_cfg = config["market"]
    views_cfg = config["views"]
    
    assets = market_cfg["tickers"]
    period = market_cfg["period"]
    rf_rate = market_cfg["risk_free_rate"]
    risk_aversion = market_cfg["risk_aversion"]
    tau = market_cfg["tau"]
    
    # 2. Descargar datos reales usando los parametros del TOML
    prices, returns = download_fixed_income_data(tickers=assets, period=period)
    
    # 3. Calcular matriz de covarianza anualizada
    cov_matrix = calculate_covariance_matrix(returns)
    
    # 4. Pesos de referencia de mercado (Equitativos para la inversa de optimizacion)
    market_weights = [1.0 / len(assets)] * len(assets)
    
    # 5. Calcular rendimientos implicitos de equilibrio (Pi)
    pi = calculate_implied_equilibrium_returns(market_weights, cov_matrix, risk_aversion=risk_aversion)
    
    # 6. Extraer matrices de vistas del TOML
    P = views_cfg["P"]
    Q = views_cfg["Q"]
    Omega = views_cfg["Omega"]
    
    # 7. Ejecutar la Formula Maestra de Black-Litterman
    mu_bl, cov_bl = black_litterman_master_formula(pi, cov_matrix, P, Q, Omega, tau=tau)
    
    # 8. Optimizar portafolios (Maximizar Sharpe Ratio)
    print("\nOptimizando portafolios con parametros dinamicos...")
    weights_eq = maximize_sharpe_ratio(pi, cov_matrix, risk_free_rate=rf_rate)
    weights_bl = maximize_sharpe_ratio(mu_bl, cov_bl, risk_free_rate=rf_rate)
    
    # 9. Mostrar reporte en pantalla
    print("\n" + "="*55)
    print("   REPORTE COMPARATIVO DE ASIGNACION DE PESOS (W)")
    print("="*55)
    for asset in assets:
        print(f"Activo: {asset}")
        print(f"  -> Peso Optimo Mercado Tradicional: {weights_eq[asset]*100:.2f}%")
        print(f"  -> Peso Optimo Ajustado BL         : {weights_bl[asset]*100:.2f}%")
        print("-"*55)
        
    # 10. Generar grafico
    plot_portfolio_comparison(assets, weights_eq, weights_bl)

if __name__ == "__main__":
    run_pipeline()
