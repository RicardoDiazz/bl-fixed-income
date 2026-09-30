import os
import pandas as pd
from src.bl_fixed_income.decomposition import run_decomposition_analysis


def test_decomposition_outputs_exist():
    run_decomposition_analysis()

    path_omega = "data/results/decomposition_omega.csv"
    path_dns = "data/results/decomposition_dns.csv"
    path_md = "configs/decomposition_analysis.md"

    assert os.path.exists(path_omega), "Falta decomposition_omega.csv"
    assert os.path.exists(path_dns), "Falta decomposition_dns.csv"
    assert os.path.exists(path_md), "Falta decomposition_analysis.md"

    df_omega = pd.read_csv(path_omega)
    df_dns = pd.read_csv(path_dns)

    assert len(df_omega) == 8, "Debe haber 8 portafolios en decomposition_omega.csv"
    assert (
        "DNS_Level" in df_dns["DNS_Factor"].values
    ), "Falta DNS_Level en decomposition_dns.csv"
