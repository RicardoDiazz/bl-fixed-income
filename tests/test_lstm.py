import numpy as np
import pandas as pd

from src.models.lstm import train_evaluate_lstm


def test_train_evaluate_lstm():
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=30, freq="D")
    df = pd.DataFrame(
        {
            "date": dates,
            "feature1": np.random.randn(30),
            "feature2": np.random.randn(30),
            "SHY_Q1": np.random.randn(30),
            "IEF_Q1": np.random.randn(30),
        }
    )

    forecasts = train_evaluate_lstm(
        df=df,
        feature_cols=["feature1", "feature2"],
        target_cols=["SHY_Q1", "IEF_Q1"],
        initial_train_size=20,
        seq_len=3,
        epochs=2,
    )

    assert isinstance(forecasts, pd.DataFrame)
    assert len(forecasts) == 10  # 30 total - 20 initial_train
    assert "pred_SHY_Q1" in forecasts.columns
    assert "actual_SHY_Q1" in forecasts.columns
    assert "pred_IEF_Q1" in forecasts.columns
    assert "actual_IEF_Q1" in forecasts.columns
    assert not forecasts.isnull().any().any()
