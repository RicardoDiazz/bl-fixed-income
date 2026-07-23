"""Script para generar pronósticos out-of-sample utilizando el modelo Transformer."""

import os

import numpy as np
import pandas as pd

from src.models.transformer import TransformerForecaster


def generate_transformer_forecasts():
    """Genera pronósticos out-of-sample alineados con el protocolo rolling del proyecto."""
    features_path = "data/processed/features.parquet"
    targets_path = "data/processed/panel_semanal.parquet"
    output_path = "data/processed/forecasts_transformer.parquet"

    if not os.path.exists(features_path) or not os.path.exists(targets_path):
        raise FileNotFoundError(
            "Faltan archivos de datos processed (features o panel_semanal)."
        )

    X = pd.read_parquet(features_path)
    y_full = pd.read_parquet(targets_path)

    # Filtrar solo las columnas de targets (_Q1, _Q2, _Q3)
    target_cols = [
        col
        for col in y_full.columns
        if any(col.endswith(q) for q in ["_Q1", "_Q2", "_Q3"])
    ]
    y = y_full[target_cols]

    # Reemplazar infinitos por NaN
    X = X.replace([np.inf, -np.inf], np.nan)
    y = y.replace([np.inf, -np.inf], np.nan)

    # Alinear índices comunes
    common_idx = X.index.intersection(y.index)
    X = X.loc[common_idx]
    y = y.loc[common_idx]

    # Imputar features (ffill + bfill para lags/fechas iniciales)
    X = X.dropna(how="all", axis=1).ffill().bfill()

    # Imputar targets (ffill ligero)
    y = y.ffill(limit=3)

    # Filtrar registros válidos
    valid_mask = y.notna().all(axis=1) & X.notna().all(axis=1)
    X_clean = X.loc[valid_mask]
    y_clean = y.loc[valid_mask]

    print(
        f"Filas originales: {len(X)} | Filas limpias para entrenamiento: {len(X_clean)}"
    )

    # Protocolo Expanding Window
    oos_periods = 217
    min_train_size = len(X_clean) - oos_periods

    if min_train_size <= 0:
        raise ValueError(
            f"El tamaño del conjunto de entrenamiento ({min_train_size}) es insuficiente para {oos_periods} periodos OOS."
        )

    forecasts_list = []
    seq_len = 4

    print(
        f"Generando pronósticos Transformer para {oos_periods} periodos out-of-sample..."
    )

    for i in range(min_train_size, len(X_clean)):
        X_train = X_clean.iloc[:i]
        y_train = y_clean.iloc[:i]

        # La ventana de entrada para predecir requiere seq_len observaciones
        X_test_seq = X_clean.iloc[i - seq_len + 1 : i + 1]

        model = TransformerForecaster(seq_len=seq_len, epochs=15, batch_size=32)
        model.fit(X_train, y_train)

        pred = model.predict(X_test_seq)
        forecasts_list.append(pred)

    forecasts = pd.concat(forecasts_list)

    # Crear carpeta si no existe y guardar
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    forecasts.to_parquet(output_path)
    print(
        f"Pronósticos Transformer guardados exitosamente en {output_path} con {len(forecasts)} registros."
    )


if __name__ == "__main__":
    generate_transformer_forecasts()
