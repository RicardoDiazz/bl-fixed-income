import os
import numpy as np
import pandas as pd


def setup_investor_views():
    """Configura las matrices P, Q y calcula Omega para Black-Litterman."""
    input_path = "data/processed/panel_semanal.parquet"
    assets = ["SHY", "IEF", "TLT"]

    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"No se encontró el archivo Parquet en {input_path}. Corre los pasos previos."
        )

    # 1. Cargar datos y calcular covarianza anualizada para calibrar Omega
    df = pd.read_parquet(input_path)
    sigma_anual = df[assets].cov() * 52

    # Escalar tau (calibración del peso de las vistas, estándar: 0.05)
    tau = 0.05

    print("--- Configurando Vistas del Inversor ---")

    # 2. Matriz Q (Vector de retornos de las vistas - Anualizados)
    # Vista 1 (Absoluta): TLT tendrá un retorno del 4.5% (0.045)
    # Vista 2 (Relativa): IEF superará a SHY por 1.5% (0.015)
    q = np.array([0.045, 0.015])

    print("\nVector Q (Retornos Esperados de las Vistas):")
    print(f"  Vista 1 (Absoluta TLT): {q[0]*100:.2f}%")
    print(f"  Vista 2 (Relativa IEF vs SHY): {q[1]*100:.2f}%")

    # 3. Matriz P (Matriz de Identificación de Activos, k x n)
    # Columnas corresponden a: [SHY, IEF, TLT]
    p = np.array(
        [
            [0, 0, 1],  # Vista 1 afectando solo a TLT
            [-1, 1, 0],  # Vista 2: IEF (+1) supera a SHY (-1)
        ]
    )

    print("\nMatriz P (Identificación de Activos afectando las vistas):")
    print(p)

    # 4. Calcular Matriz Omega (Incertidumbre de las vistas usando He & Litterman)
    # Omega = diag(P * (tau * Sigma) * P^T)
    omega = np.zeros((len(q), len(q)))

    for i in range(len(q)):
        p_i = p[i, :]
        # Varianza proyectada de la vista i
        omega[i, i] = tau * np.dot(p_i, np.dot(sigma_anual.values, p_i))

    print("\nMatriz Omega (Incertidumbre / Varianza del Error de las Vistas):")
    print(omega)

    return p, q, omega


if __name__ == "__main__":
    setup_investor_views()