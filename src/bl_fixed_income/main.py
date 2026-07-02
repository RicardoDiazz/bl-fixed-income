from bl_fixed_income.data_loader import download_fixed_income_data
from bl_fixed_income.analytics import calculate_covariance_matrix, calculate_implied_equilibrium_returns, black_litterman_master_formula

def run_pipeline():
    print("==========================================================")
    print("   EJECUTANDO PIPELINE: MODELO BLACK-LITTERMAN RENTA FIJA")
    print("==========================================================\n")
    
    # 1. Descargar datos reales de mercado (Ultimos 5 anos)
    assets = ["SHY", "IEF", "TLT"]
    prices, returns = download_fixed_income_data(tickers=assets, period="5y")
    
    # 2. Calcular matriz de covarianza anualizada real
    cov_matrix = calculate_covariance_matrix(returns)
    
    # 3. Asumir pesos de equilibrio del mercado (Portafolio equitativo de referencia)
    market_weights = [1/3, 1/3, 1/3]
    
    # 4. Calcular rendimientos implicitos de equilibrio del mercado (Pi)
    pi = calculate_implied_equilibrium_returns(market_weights, cov_matrix)
    
    # 5. Configurar Vistas del Analista (Opiniones Subjetivas)
    # Vista: "Los bonos de largo plazo (TLT) tendran un rendimiento absoluto del 4.5% anual"
    P = [[0, 0, 1]] 
    Q = [0.045]      
    Omega = [[0.00005]] # Nivel de incertidumbre/varianza de la opinion
    
    # 6. Ejecutar la Formula Maestra de Black-Litterman
    mu_bl, cov_bl = black_litterman_master_formula(pi, cov_matrix, P, Q, Omega)
    
    # 7. Mostrar resultados comparativos
    print("\n" + "="*50)
    print("   RESULTADOS COMPARATIVOS DE RENDIMIENTOS ANUALES")
    print("="*50)
    for asset in assets:
        print(f"Activo: {asset}")
        print(f"  -> Rendimiento de Equilibrio Mercado (Pi): {pi[asset]*100:.4f}%")
        print(f"  -> Rendimiento Ajustado Black-Litterman (Mu): {mu_bl[asset]*100:.4f}%")
        print("-"*50)

if __name__ == "__main__":
    run_pipeline()
