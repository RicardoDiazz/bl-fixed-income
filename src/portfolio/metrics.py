import os
import numpy as np
import pandas as pd


def calculate_portfolio_metrics(
    returns: pd.Series, risk_free_rate: float = 0.02, periods_per_year: int = 52
) -> dict:
    s = returns.dropna()
    if len(s) == 0:
        return {
            "Annualized_Return": 0.0,
            "Annualized_Vol": 0.0,
            "Sharpe_Ratio": 0.0,
            "Max_Drawdown": 0.0,
        }

    ann_return = float(s.mean() * periods_per_year)
    ann_vol = float(s.std() * np.sqrt(periods_per_year))
    sharpe = (
        float((ann_return - risk_free_rate) / ann_vol)
        if (ann_vol != 0 and not np.isnan(ann_vol))
        else 0.0
    )

    cum_returns = (1 + s).cumprod()
    peak = cum_returns.cummax()
    drawdown = (cum_returns - peak) / peak
    max_drawdown = float(drawdown.min()) if len(drawdown) > 0 else 0.0

    return {
        "Annualized_Return": ann_return,
        "Annualized_Vol": ann_vol,
        "Sharpe_Ratio": sharpe,
        "Max_Drawdown": max_drawdown,
    }


def generate_full_and_subperiod_metrics():
    os.makedirs("data/results", exist_ok=True)

    data_path = "data/processed/panel_semanal.parquet"
    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"No se encontro el archivo base de datos en {data_path}"
        )

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

    # 1. Periodo Completo
    full_metrics = []
    for p in portfolios:
        m = calculate_portfolio_metrics(df_returns[p])
        m["Portfolio"] = p
        full_metrics.append(m)

    df_full = pd.DataFrame(full_metrics).set_index("Portfolio")
    df_full.to_csv("data/results/metrics_full.csv")

    # 2. Sub-periodos
    n_splits = 6
    split_size = int(np.ceil(len(df_returns) / n_splits))
    sub_metrics = []

    for idx in range(n_splits):
        start_idx = idx * split_size
        end_idx = min((idx + 1) * split_size, len(df_returns))
        sub_df = df_returns.iloc[start_idx:end_idx]

        if len(sub_df) > 0:
            for p in portfolios:
                m = calculate_portfolio_metrics(sub_df[p])
                m["Subperiod"] = f"Subperiod_{idx+1}"
                m["Portfolio"] = p
                sub_metrics.append(m)

    df_sub = pd.DataFrame(sub_metrics)
    df_sub.to_csv("data/results/metrics_subperiods.csv", index=False)

    print("Archivos CSV de metricas generados con exito.")


if __name__ == "__main__":
    generate_full_and_subperiod_metrics()
