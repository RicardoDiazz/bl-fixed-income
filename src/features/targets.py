import os

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller


def build_targets_and_analyze():
    """Construye targets Q1, Q2, Q3 (shifts futuros) y genera reporte ADF limpiando nulos."""
    input_path = "data/processed/panel_semanal.parquet"
    output_path = "data/processed/panel_semanal.parquet"
    report_path = "configs/targets_analysis.md"

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No se encontró el archivo en {input_path}")

    df = pd.read_parquet(input_path)
    assets = ["SHY", "IEF", "TLT"]

    print("--- Construyendo Targets Predictivos ---")

    markdown_report = "# Análisis Económico y Estacionariedad (Test ADF)\n\n"
    markdown_report += "Este documento presenta la validación formal de las variables "
    markdown_report += (
        "objetivo (targets) para evitar problemas de raíces unitarias.\n\n"
    )

    # Horizontes: Q1 (1 sem), Q2 (2 sem), Q3 (4 sem)
    horizons = {"Q1": -1, "Q2": -2, "Q3": -4}

    for asset in assets:
        ret_col = f"{asset}_ret"
        if ret_col not in df.columns:
            df[ret_col] = np.log(df[asset] / df[asset].shift(1))

        markdown_report += f"## Activo: {asset}\n"

        for label, shift_val in horizons.items():
            target_name = f"{asset}_{label}"
            # shift(-1) mueve el retorno del futuro al registro actual
            df[target_name] = df[ret_col].shift(shift_val)

            # ¡SOLUCIÓN AQUÍ! Eliminamos NaNs e Infs de la serie antes de meterla al modelo
            series_to_test = df[target_name].replace([np.inf, -np.inf], np.nan).dropna()

            if len(series_to_test) > 10:
                # Usamos maxlag de forma explícita o dejamos que remueva nulos internos
                try:
                    result = adfuller(series_to_test, autolag="AIC")
                    adf_stat = result[0]
                    p_value = result[1]
                    crit_values = result[4]

                    is_stationary = p_value < 0.05
                    status_str = (
                        "Estacionaria (Rechaza H0)"
                        if is_stationary
                        else "No Estacionaria (Posee Raíz Unitaria)"
                    )

                    print(
                        f"Target {target_name} -> p-value: {p_value:.4f} | {status_str}"
                    )

                    markdown_report += (
                        f"### Target {label} ({abs(shift_val)} semanas adelante)\n"
                    )
                    markdown_report += f"- **Nombre de variable:** `{target_name}`\n"
                    markdown_report += f"- **Estadístico ADF:** `{adf_stat:.4f}`\n"
                    markdown_report += f"- **p-value:** `{p_value:.4e}`\n"
                    markdown_report += f"- **Resultado:** *{status_str}*\n"
                    markdown_report += f"- **Valores Críticos:** 1%: `{crit_values['1%']:.2f}`, 5%: `{crit_values['5%']:.2f}`\n\n"
                except Exception as e:
                    print(f"Error analizando {target_name}: {e}")

    # Guardar el DataFrame con los targets incorporados
    df.to_parquet(output_path, index=True)
    print(f"\nDataFrame actualizado guardado en {output_path}")

    # Guardar reporte técnico en configs/
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(markdown_report)
    print(f"Reporte de interpretación económica generado en {report_path}\n")


if __name__ == "__main__":
    build_targets_and_analyze()
