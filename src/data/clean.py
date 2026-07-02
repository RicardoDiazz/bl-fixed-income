import os

import pandas as pd


def clean_and_process_data():
    """Lee los datos crudos, calcula retornos y exporta a formato Parquet."""
    raw_path = "data/raw/precios_crudos.csv"
    processed_dir = "data/processed"
    output_path = os.path.join(processed_dir, "panel_semanal.parquet")

    print(f"Leyendo datos crudos desde: {raw_path}")

    if not os.path.exists(raw_path):
        raise FileNotFoundError(
            f"No se encontró el archivo crudo en {raw_path}. Ejecuta download.py primero."
        )

    # 1. Leer datos asegurando que la fecha sea el índice
    df = pd.read_csv(raw_path, parse_dates=["Date"], index_col="Date")

    # 2. Resamplear a frecuencia semanal (tomando el último precio de la semana)
    # Esto suaviza el ruido diario y cumple con el formato 'panel_semanal'
    df_weekly = df.resample("W").last()

    # 3. Calcular retornos logarítmicos o porcentuales (usaremos porcentuales para BL)
    df_returns = df_weekly.pct_change()

    # 4. Eliminar la primera fila que queda con NaNs debido al cálculo de retornos
    df_clean = df_returns.dropna()

    # Asegurar que la carpeta de destino existe
    os.makedirs(processed_dir, exist_ok=True)

    # 5. Exportar a formato Parquet (eficiente en almacenamiento y lectura)
    df_clean.to_parquet(output_path)
    print("¡Procesamiento completado con éxito!")
    print(f"Archivo Parquet guardado en: {output_path}")
    print(f"Dimensiones del dataset: {df_clean.shape}")


if __name__ == "__main__":
    clean_and_process_data()
