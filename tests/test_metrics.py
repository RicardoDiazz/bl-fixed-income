import os
import pandas as pd
from src.portfolio.metrics import (
    calculate_portfolio_metrics,
    generate_full_and_subperiod_metrics,
)


def test_calculate_portfolio_metrics_structure():
    returns = pd.Series([0.01, -0.005, 0.008, 0.012, -0.003])
    metrics = calculate_portfolio_metrics(returns)

    assert "Annualized_Return" in metrics
    assert "Annualized_Vol" in metrics
    assert "Sharpe_Ratio" in metrics
    assert "Max_Drawdown" in metrics
    assert isinstance(metrics["Sharpe_Ratio"], float)


def test_generated_csv_files_exist():
    generate_full_and_subperiod_metrics()

    path_full = "data/results/metrics_full.csv"
    path_sub = "data/results/metrics_subperiods.csv"

    assert os.path.exists(path_full), "Falta el archivo metrics_full.csv"
    assert os.path.exists(path_sub), "Falta el archivo metrics_subperiods.csv"

    df_full = pd.read_csv(path_full)
    df_sub = pd.read_csv(path_sub)

    assert (
        len(df_full) == 8
    ), "Debe haber exactamente 8 portafolios en el periodo completo"
    assert (
        "Subperiod_6" in df_sub["Subperiod"].values
    ), "Faltan los 6 subperiodos en metrics_subperiods.csv"
