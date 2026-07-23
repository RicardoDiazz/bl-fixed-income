import os

import numpy as np
import pandas as pd


def compute_log_returns():
    """Calcula los retornos logarítmicos a partir de los precios limpios."""
    input_path = "data/processed/panel_semanal.parquet"
    output_path = (
        "data/processed/panel_semanal.parquet"  # Sobrescribimos agregando las columnas
    )

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No se encontró el archivo en {input_path}")

    df = pd.read_parquet(input_path)
    assets = ["SHY", "IEF", "TLT"]

    print("--- Calculando Retornos Logarítmicos ---")
    for asset in assets:
        # Retorno logarítmico: ln(P_t / P_{t-1})
        df[f"{asset}_ret"] = np.log(df[asset] / df[asset].shift(1))
        print(f"Retornos calculados para: {asset}")

    # Guardar de nuevo en el archivo Parquet
    df.to_parquet(output_path, index=True)
    print(f"Datos guardados exitosamente en {output_path}\n")


if __name__ == "__main__":
    compute_log_returns()
