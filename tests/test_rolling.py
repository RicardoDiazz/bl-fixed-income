import numpy as np
import pandas as pd

from src.models.metrics import calculate_mae, calculate_rmse
from src.models.rolling import ExpandingWindowSplitter


def test_expanding_window_split():
    df = pd.DataFrame({"value": np.arange(100)})

    splitter = ExpandingWindowSplitter(initial_train_size=60, step_size=10)
    splits = list(splitter.split(df))

    # Verificar cantidad de iteraciones
    assert len(splits) == 4

    # Verificar primera iteración
    train_0, test_0 = splits[0]
    assert len(train_0) == 60
    assert len(test_0) == 10
    assert train_0[-1] == 59
    assert test_0[0] == 60

    # Verificar última iteración
    train_last, test_last = splits[-1]
    assert len(train_last) == 90
    assert len(test_last) == 10


def test_metrics_calculation():
    y_true = np.array([1.0, 2.0, 3.0])
    y_pred = np.array([1.0, 2.5, 2.5])

    rmse = calculate_rmse(y_true, y_pred)
    mae = calculate_mae(y_true, y_pred)

    assert isinstance(rmse, float)
    assert isinstance(mae, float)
    assert round(mae, 2) == 0.33
