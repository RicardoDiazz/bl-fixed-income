"""Módulo para el modelo baseline Transformer en Fixed Income."""

from typing import Optional

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


class PyTorchTransformer(nn.Module):
    """Arquitectura Transformer Encoder para series de tiempo."""

    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        d_model: int = 32,
        nhead: int = 2,
        num_layers: int = 1,
    ):
        super().__init__()
        self.input_proj = nn.Linear(input_dim, d_model)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=nhead, dim_feedforward=64, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc_out = nn.Linear(d_model, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x shape: (batch_size, sequence_length, features)
        x = self.input_proj(x)
        out = self.transformer(x)
        out = out[:, -1, :]  # Tomar el último paso de tiempo de la secuencia
        return self.fc_out(out)


class TransformerForecaster:
    """Encapsula el entrenamiento y predicción del modelo Transformer PyTorch."""

    def __init__(
        self,
        seq_len: int = 4,
        epochs: int = 20,
        lr: float = 0.001,
        batch_size: int = 16,
    ):
        self.seq_len = seq_len
        self.epochs = epochs
        self.lr = lr
        self.batch_size = batch_size
        self.model: Optional[PyTorchTransformer] = None
        self.target_cols = []
        self.feature_cols = []

    def _create_sequences(self, X: np.ndarray, y: np.ndarray):
        X_seq, y_seq = [], []
        for i in range(len(X) - self.seq_len + 1):
            X_seq.append(X[i : i + self.seq_len])
            y_seq.append(y[i + self.seq_len - 1])
        return np.array(X_seq), np.array(y_seq)

    def fit(self, X: pd.DataFrame, y: pd.DataFrame) -> "TransformerForecaster":
        """Entrena el modelo Transformer sobre los datos proporcionados."""
        self.feature_cols = list(X.columns)
        self.target_cols = list(y.columns)

        X_val = X.values
        y_val = y.values

        if len(X_val) < self.seq_len:
            raise ValueError(
                f"El número de muestras ({len(X_val)}) debe ser >= seq_len ({self.seq_len})."
            )

        X_seq, y_seq = self._create_sequences(X_val, y_val)

        X_tensor = torch.tensor(X_seq, dtype=torch.float32)
        y_tensor = torch.tensor(y_seq, dtype=torch.float32)

        dataset = TensorDataset(X_tensor, y_tensor)
        loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

        self.model = PyTorchTransformer(
            input_dim=len(self.feature_cols), output_dim=len(self.target_cols)
        )
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        criterion = nn.MSELoss()

        self.model.train()
        for _ in range(self.epochs):
            for batch_x, batch_y in loader:
                optimizer.zero_grad()
                out = self.model(batch_x)
                loss = criterion(out, batch_y)
                loss.backward()
                optimizer.step()

        return self

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """Genera predicciones utilizando el contexto de la ventana secuencial."""
        if self.model is None:
            raise RuntimeError("El modelo no ha sido entrenado. Ejecuta fit() primero.")

        self.model.eval()
        X_val = X.values[-self.seq_len :]
        X_seq = np.array([X_val])
        X_tensor = torch.tensor(X_seq, dtype=torch.float32)

        with torch.no_grad():
            preds = self.model(X_tensor).numpy()

        # Retornar DataFrame alineado al último índice de entrada
        return pd.DataFrame(preds, index=[X.index[-1]], columns=self.target_cols)
