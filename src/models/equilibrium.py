import os
import numpy as np
import pandas as pd


def estimate_market_equilibrium():
    """Calcula los pesos de mercado, aversión al riesgo y retornos implícitos."""
    input_path = "data/processed/panel_semanal.parquet"

    print(f"Cargando datos desde: {input_path}")
    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"No se encontró el archivo Parquet en {input_path}. Corre los pasos previos."
        )

    df = pd.read_parquet(input_path)

    # 1. Definir Capitalizaciones de Mercado (en Billones de USD)
    market_caps = {"SHY": 82.5, "IEF": 48.3, "TLT": 45.2}

    # Calcular Pesos de Mercado (w_mkt)
    assets = list(market_caps.keys())
    caps_vector = np.array([market_caps[asset] for asset in assets])
    w_mkt = caps_vector / np.sum(caps_vector)

    print("\n--- Pesos del Portafolio de Mercado (w_mkt) ---")
    for asset, weight in zip(assets, w_mkt):
        print(f"{asset}: {weight:.4f} ({weight * 100:.2f}%)")

    # 2. Calcular Matriz de Covarianza Semanal y Anualizarla (52 semanas)
    sigma_semanal = df[assets].cov()
    sigma_anual = sigma_semanal * 52

    # 3. Estimar Coeficiente de Aversión al Riesgo (Lambda)
    # Asumimos una prima de riesgo de mercado de renta fija (E(Rm) - Rf) de 2.5%
    market_premium = 0.025
    variance_mkt = np.dot(w_mkt.T, np.dot(sigma_anual.values, w_mkt))
    lambda_mkt = market_premium / variance_mkt

    print(f"\nVarianza Anualizada del Mercado (sigma^2_m): {variance_mkt:.6f}")
    print(f"Coeficiente de Aversión al Riesgo (Lambda): {lambda_mkt:.4f}")

    # 4. Calcular Vector de Retornos Implícitos de Equilibrio (Pi = Lambda * Sigma * w_mkt)
    pi = lambda_mkt * np.dot(sigma_anual.values, w_mkt)

    print("\n--- Vector de Retornos Implícitos de Equilibrio Anualizados (Pi) ---")
    for asset, r_implied in zip(assets, pi):
        print(f"{asset}: {r_implied:.4f} ({r_implied * 100:.2f}%)")

    # Guardar resultados en variables o archivos si fuera necesario para la Semana 5
    return w_mkt, pi, sigma_anual


if __name__ == "__main__":
    estimate_market_equilibrium()