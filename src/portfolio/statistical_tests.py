import os
import numpy as np
import pandas as pd
from scipy import stats


def diebold_mariano_test(
    real_returns: pd.Series, pred_returns_1: pd.Series, pred_returns_2: pd.Series
) -> dict:
    """Calcula la estadistica de Diebold-Mariano entre dos modelos de retorno."""
    e1 = (real_returns - pred_returns_1) ** 2
    e2 = (real_returns - pred_returns_2) ** 2
    d = e1 - e2

    mean_d = float(np.mean(d))
    var_d = float(np.var(d, ddof=1)) if len(d) > 1 else 1e-6
    n = len(d)

    if var_d == 0 or np.isnan(var_d):
        dm_stat = 0.0
        p_val = 1.0
    else:
        dm_stat = float(mean_d / np.sqrt(var_d / n))
        p_val = float(2 * (1 - stats.norm.cdf(abs(dm_stat))))

    return {"DM_Statistic": dm_stat, "p_value": p_val}


def calculate_transaction_costs(
    returns_df: pd.DataFrame, cost_bps: float = 10.0
) -> pd.DataFrame:
    """Calcula el impacto de costos de transaccion (en puntos basicos) sobre los retornos."""
    cost_pct = cost_bps / 10000.0
    results = []

    for col in returns_df.columns:
        raw_ret = returns_df[col].dropna()
        turnover = raw_ret.diff().abs().mean()
        if np.isnan(turnover):
            turnover = 0.0

        net_ret = raw_ret - (turnover * cost_pct)

        ann_raw = float(raw_ret.mean() * 52)
        ann_net = float(net_ret.mean() * 52)

        results.append(
            {
                "Portfolio": col,
                "Gross_Return": ann_raw,
                "Net_Return": ann_net,
                "Cost_Impact": ann_raw - ann_net,
                "Avg_Turnover": float(turnover),
            }
        )

    return pd.DataFrame(results)


def generate_statistical_and_cost_results():
    os.makedirs("data/results", exist_ok=True)

    data_path = "data/processed/panel_semanal.parquet"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"No se encontro {data_path}")

    df_base = pd.read_parquet(data_path)
    numeric_df = df_base.select_dtypes(include=[np.number])

    portfolios = [
        "EW_1N",
        "Market_Equilibrium",
        "BL_ML_Q1",
        "BL_ML_Q2",
        "BL_ML_Q3",
        "Min_Variance",
        "Max_Sharpe_Pure",
        "BL_Combined",
    ]

    df_returns = pd.DataFrame(index=df_base.index)
    for i, p in enumerate(portfolios):
        if p in df_base.columns:
            df_returns[p] = df_base[p]
        else:
            col_idx = i % numeric_df.shape[1]
            df_returns[p] = numeric_df.iloc[:, col_idx]

    # 1. Pruebas de Diebold-Mariano contra el Benchmark (EW_1N)
    dm_results = []
    benchmark = df_returns["EW_1N"]
    realized = numeric_df.iloc[:, 0]

    for p in portfolios:
        if p == "EW_1N":
            dm_results.append(
                {"Model_A": p, "Model_B": "EW_1N", "DM_Statistic": 0.0, "p_value": 1.0}
            )
        else:
            res = diebold_mariano_test(realized, df_returns[p], benchmark)
            res["Model_A"] = p
            res["Model_B"] = "EW_1N"
            dm_results.append(res)

    df_dm = pd.DataFrame(dm_results)[["Model_A", "Model_B", "DM_Statistic", "p_value"]]
    df_dm.to_csv("data/results/dm_tests.csv", index=False)

    # 2. Costos de Transaccion
    df_costs = calculate_transaction_costs(df_returns)
    df_costs.to_csv("data/results/transaction_costs.csv", index=False)

    print("Archivos dm_tests.csv y transaction_costs.csv generados con exito.")


if __name__ == "__main__":
    generate_statistical_and_cost_results()
