import os
import numpy as np
import pandas as pd


def build_lagged_features():
    """Genera variables rezagadas (lags) para evitar leaks y congelar el dataset."""
    input_path = "data/processed/panel_semanal.parquet"
    output_path = "data/processed/features.parquet"

    print("--- Iniciando Construcción de Features (Lags) ---")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No se encontró el archivo base en {input_path}")

    df = pd.read_parquet(input_path)
    assets = ["SHY", "IEF", "TLT"]

    # Hacer una copia limpia solo con las columnas base y retornos que necesitamos
    feature_cols = []
    for asset in assets:
        ret_col = f"{asset}_ret"
        if ret_col not in df.columns:
            df[ret_col] = np.log(df[asset] / df[asset].shift(1))

    # Creamos rezagos (lags) históricos: t-1, t-2, t-3 para cada activo
    # Esto es lo que el modelo usará en tiempo real para predecir el futuro
    lags = [1, 2, 3]

    for asset in assets:
        ret_col = f"{asset}_ret"
        for lag in lags:
            lag_name = f"{asset}_ret_lag_{lag}"
            df[lag_name] = df[ret_col].shift(lag)
            feature_cols.append(lag_name)
            print(f"Feature creado: {lag_name} (Retorno t-{lag})")

    # Guardar el DataFrame completo (con los targets y las nuevas features de rezago)
    # en la ruta específica solicitada por el entregable
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path, index=True)

    print(f"\nMatriz de variables completada exitosamente.")
    print(f"Dataset congelado guardado en: {output_path}\n")


if __name__ == "__main__":
    build_lagged_features()