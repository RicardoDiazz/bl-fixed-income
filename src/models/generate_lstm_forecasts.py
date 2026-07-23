from pathlib import Path

import numpy as np
import pandas as pd

from src.models.lstm import train_evaluate_lstm


def main():
    print("Cargando dataset para LSTM...")
    data_path = Path("data/processed/features.parquet")
    if not data_path.exists():
        data_path = Path("data/processed/dataset.parquet")

    df = pd.read_parquet(data_path)

    # Identificar targets de cuantiles
    target_cols = [
        "SHY_Q1",
        "SHY_Q2",
        "SHY_Q3",
        "IEF_Q1",
        "IEF_Q2",
        "IEF_Q3",
        "TLT_Q1",
        "TLT_Q2",
        "TLT_Q3",
    ]
    target_cols = [c for c in target_cols if c in df.columns]

    feature_cols = [
        col for col in df.columns if col not in target_cols and col != "date"
    ]

    # Reemplazar valores infinitos por NaN
    df = df.replace([np.inf, -np.inf], np.nan)

    # Rellenar targets si hay un desfase ligero en las fechas (mismísima lógica que Ridge)
    df[target_cols] = df[target_cols].ffill(limit=3)

    # Descartar filas donde todavía no haya targets suficientes
    df_clean = df.dropna(subset=target_cols, how="any").copy()

    # Rellenar features remanentes
    df_clean[feature_cols] = df_clean[feature_cols].ffill().bfill().fillna(0)

    print(
        f"Filas originales: {len(df)} | Filas limpias listas para training: {len(df_clean)}"
    )
    print(
        f"Procesando LSTM con {len(feature_cols)} features y {len(target_cols)} targets..."
    )

    initial_train_size = int(len(df_clean) * 0.6)

    forecasts = train_evaluate_lstm(
        df=df_clean,
        feature_cols=feature_cols,
        target_cols=target_cols,
        initial_train_size=initial_train_size,
        step=1,
        seq_len=4,
        epochs=15,
        hidden_dim=32,
    )

    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "forecasts_lstm.parquet"

    forecasts.to_parquet(output_path)
    print(
        f"Pronósticos guardados exitosamente en {output_path} con {len(forecasts)} registros."
    )


if __name__ == "__main__":
    main()
