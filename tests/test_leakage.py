import os

import pandas as pd


def test_no_data_leakage():
    """Verifica formalmente la ausencia de leakage temporal en las variables lagged usando iloc."""
    file_path = "data/processed/features.parquet"
    assert os.path.exists(file_path), "El archivo Parquet de características no existe."

    df = pd.read_parquet(file_path)
    assets = ["SHY", "IEF", "TLT"]

    # Asegurar orden cronológico ascendente antes de validar
    df = df.sort_index()

    for asset in assets:
        ret_col = f"{asset}_ret"
        lag_1_col = f"{asset}_ret_lag_1"

        if ret_col in df.columns and lag_1_col in df.columns:
            # Creamos un dataframe temporal sin eliminar índices completos para no perder la secuencia
            # Buscaremos una fila en donde tanto el presente (t) como el lag_1 (t) tengan datos válidos
            valid_rows = df[[ret_col, lag_1_col]].notna().all(axis=1)
            valid_indices = df[valid_rows].index

            if len(valid_indices) > 5:
                # Tomamos una fecha de control intermedia del dataset original
                fecha_presente = valid_indices[10]

                # Localizamos su posición numérica entera en el DataFrame ordenado
                pos_presente = df.index.get_loc(fecha_presente)
                pos_pasado = (
                    pos_presente - 1
                )  # La semana inmediatamente anterior en el tiempo

                # Obtenemos los valores correspondientes
                val_original_pasado = df.iloc[pos_pasado][ret_col]
                val_lagged_presente = df.iloc[pos_presente][lag_1_col]

                # El lag_1 hoy (t) debe ser idéntico al retorno original de la fila anterior (t-1)
                assert val_original_pasado == val_lagged_presente, (
                    f"🚨 ALERTA DE LEAKAGE REAL DETECTADA: "
                    f"El lag_1 en {fecha_presente} no coincide con el retorno anterior."
                )
