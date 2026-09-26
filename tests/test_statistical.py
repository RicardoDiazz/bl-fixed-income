import os
import pandas as pd
from src.portfolio.statistical_tests import (
    generate_statistical_and_cost_results,
    diebold_mariano_test,
)


def test_diebold_mariano_structure():
    s1 = pd.Series([0.01, 0.02, -0.01, 0.005])
    s2 = pd.Series([0.008, 0.019, -0.009, 0.004])
    real = pd.Series([0.011, 0.021, -0.012, 0.006])

    res = diebold_mariano_test(real, s1, s2)
    assert "DM_Statistic" in res
    assert "p_value" in res
    assert isinstance(res["p_value"], float)


def test_statistical_output_files_exist():
    generate_statistical_and_cost_results()

    path_dm = "data/results/dm_tests.csv"
    path_costs = "data/results/transaction_costs.csv"

    assert os.path.exists(path_dm), "Falta el archivo dm_tests.csv"
    assert os.path.exists(path_costs), "Falta el archivo transaction_costs.csv"

    df_dm = pd.read_csv(path_dm)
    df_costs = pd.read_csv(path_costs)

    assert len(df_dm) == 8, "Debe haber 8 comparaciones en dm_tests.csv"
    assert (
        "Net_Return" in df_costs.columns
    ), "Falta la columna Net_Return en transaction_costs.csv"
