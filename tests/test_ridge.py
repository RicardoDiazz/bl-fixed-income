import numpy as np
import pandas as pd

from src.models.ridge import train_evaluate_ridge


def test_ridge_expanding_window():
    dates = pd.date_range("2024-01-01", periods=100)
    data = {
        "feat1": np.random.randn(100),
        "feat2": np.random.randn(100),
        "target1": np.random.randn(100),
        "target2": np.random.randn(100),
    }
    df = pd.DataFrame(data, index=dates)

    results = train_evaluate_ridge(
        df=df,
        feature_cols=["feat1", "feat2"],
        target_cols=["target1", "target2"],
        initial_train_size=50,
    )

    assert not results.empty
    assert len(results) == 50
    assert "pred_target1" in results.columns
    assert "actual_target1" in results.columns
