import pandas as pd
from sklearn.linear_model import Ridge

from src.models.rolling import ExpandingWindowSplitter


def train_evaluate_ridge(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_cols: list[str],
    initial_train_size: int,
    alpha: float = 1.0,
) -> pd.DataFrame:
    """Entrena un modelo Ridge usando el protocolo Expanding Window.

    Genera los pronosticos fuera de muestra (out-of-sample).
    """
    splitter = ExpandingWindowSplitter(initial_train_size=initial_train_size)
    forecast_records = []

    X = df[feature_cols].values
    Y = df[target_cols].values

    for train_idx, test_idx in splitter.split(df):
        X_train, Y_train = X[train_idx], Y[train_idx]
        X_test = X[test_idx]

        model = Ridge(alpha=alpha)
        model.fit(X_train, Y_train)

        preds = model.predict(X_test)

        for i, idx in enumerate(test_idx):
            record = {"date": df.index[idx]}
            for j, col in enumerate(target_cols):
                record[f"pred_{col}"] = preds[i, j]
                record[f"actual_{col}"] = Y[idx, j]
            forecast_records.append(record)

    return pd.DataFrame(forecast_records).set_index("date")
