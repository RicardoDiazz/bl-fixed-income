import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


class LSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_layers=1):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
        )
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # x shape: (batch_size, seq_len, input_dim)
        out, _ = self.lstm(x)
        # Tomamos el último paso temporal de la secuencia
        out = self.fc(out[:, -1, :])
        return out


def train_evaluate_lstm(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_cols: list[str],
    initial_train_size: int,
    step: int = 1,
    seq_len: int = 4,
    hidden_dim: int = 32,
    epochs: int = 20,
    lr: float = 0.005,
    batch_size: int = 16,
) -> pd.DataFrame:
    """Entrena y evalúa un modelo LSTM usando un esquema Expanding Window."""
    forecasts = []

    # Fijar semillas para reproducibilidad
    torch.manual_seed(42)
    np.random.seed(42)

    n_samples = len(df)

    for i in range(initial_train_size, n_samples, step):
        train_data = df.iloc[:i]
        test_data = df.iloc[i : i + step]

        if len(train_data) <= seq_len:
            continue

        X_train_raw = train_data[feature_cols].values
        y_train_raw = train_data[target_cols].values

        # Escalamiento Z-score con estadísticas de TRAIN únicamente (evita data leakage)
        x_mean, x_std = X_train_raw.mean(axis=0), X_train_raw.std(axis=0) + 1e-8
        y_mean, y_std = y_train_raw.mean(axis=0), y_train_raw.std(axis=0) + 1e-8

        X_train_scaled = (X_train_raw - x_mean) / x_std
        y_train_scaled = (y_train_raw - y_mean) / y_std

        # Construir secuencias tridimensionales (samples, seq_len, features)
        X_seq, y_seq = [], []
        for j in range(seq_len, len(X_train_scaled)):
            X_seq.append(X_train_scaled[j - seq_len : j])
            y_seq.append(y_train_scaled[j])

        X_seq = torch.tensor(np.array(X_seq), dtype=torch.float32)
        y_seq = torch.tensor(np.array(y_seq), dtype=torch.float32)

        dataset = TensorDataset(X_seq, y_seq)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        # Inicializar modelo
        model = LSTMModel(
            input_dim=len(feature_cols),
            hidden_dim=hidden_dim,
            output_dim=len(target_cols),
        )
        optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        criterion = nn.MSELoss()

        # Entrenamiento
        model.train()
        for _ in range(epochs):
            for bx, by in loader:
                optimizer.zero_grad()
                out = model(bx)
                loss = criterion(out, by)
                loss.backward()
                optimizer.step()

        # Predicción Out-Of-Sample para test_data
        model.eval()
        history_X = pd.concat([train_data, test_data])[feature_cols].values
        history_scaled = (history_X - x_mean) / x_std

        X_test_seq = history_scaled[-seq_len - len(test_data) : -len(test_data)]
        X_test_tensor = torch.tensor(X_test_seq, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            pred_scaled = model(X_test_tensor).numpy()[0]

        # Desescalar predicción
        pred = pred_scaled * y_std + y_mean
        actual = test_data[target_cols].values[0]

        row_dict = {}
        if "date" in df.columns:
            row_dict["date"] = test_data["date"].values[0]
        else:
            row_dict["date"] = test_data.index[0]

        for idx, target in enumerate(target_cols):
            row_dict[f"pred_{target}"] = pred[idx]
            row_dict[f"actual_{target}"] = actual[idx]

        forecasts.append(row_dict)

    result_df = pd.DataFrame(forecasts)
    if "date" in result_df.columns:
        result_df.set_index("date", inplace=True)

    return result_df
