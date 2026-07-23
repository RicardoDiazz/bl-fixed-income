import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Configuración estética profesional para los gráficos
sns.set_theme(style="whitegrid")
plt.rcParams.update({"figure.max_open_warning": 50, "font.size": 10})


def run_exploratory_data_analysis():
    """Genera análisis descriptivo y gráficos estadísticos de los ETFs."""
    input_path = "data/processed/panel_semanal.parquet"
    output_dir = "reports/figures"

    print(f"Cargando datos procesados desde: {input_path}")
    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"No se encontró el archivo Parquet en {input_path}. Ejecuta clean.py primero."
        )

    df = pd.read_parquet(input_path)

    # Mostrar estadísticas descriptivas básicas en consola para control
    print("\n--- Estadísticas Descriptivas de los Retornos Semanales ---")
    print(df.describe())

    # Asegurar que la carpeta de reportes existe
    os.makedirs(output_dir, exist_ok=True)

    # 1. GRÁFICO: Retornos Acumulados (Evolución histórica)
    plt.figure(figsize=(10, 5))
    # Retorno acumulado compuesto: (1 + r).cumprod() - 1
    df_cum = (1 + df).cumprod() - 1
    for col in df_cum.columns:
        plt.plot(df_cum.index, df_cum[col], label=col, linewidth=1.5)
    plt.title("Evolución Histórica de los Retornos Acumulados (Desde 2010)")
    plt.xlabel("Fecha")
    plt.ylabel("Retorno Acumulado")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "1_retornos_acumulados.png"), dpi=300)
    plt.close()

    # 2. GRÁFICO: Histogramas y KDE (Análisis de Distribución / Colas Pesadas)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)
    for i, col in enumerate(df.columns):
        sns.histplot(
            df[col], kde=True, ax=axes[i], color="skyblue", stat="density", bins=40
        )
        axes[i].set_title(f"Distribución de Retornos: {col}")
        axes[i].set_xlabel("Retorno Semanal")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "2_distribucion_retornos.png"), dpi=300)
    plt.close()

    # 3. GRÁFICO: Matriz de Correlación (Mapa de Calor)
    plt.figure(figsize=(6, 5))
    matriz_corr = df.corr()
    sns.heatmap(
        matriz_corr,
        annot=True,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        fmt=".3f",
        linewidths=0.5,
    )
    plt.title("Matriz de Correlación de Retornos Semanales")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "3_matriz_correlacion.png"), dpi=300)
    plt.close()

    print(f"\n¡EDA completado con éxito! Gráficos guardados en: {output_dir}")


if __name__ == "__main__":
    run_exploratory_data_analysis()

# ==============================================================================
# SECCIÓN SEMANA 9: PRONÓSTICOS Y EVALUACIÓN DE MODELOS (OUT-OF-SAMPLE)
# ==============================================================================
st.markdown("---")
st.markdown("## 📈 Pronósticos y Evaluación de Modelos OOS")
st.markdown("Comparativa de rendimiento en la ventana de validación rodante para cuantiles (Q1, Q2, Q3).")

try:
    df_metrics = pd.read_csv("data/processed/comparison_baselines.csv")
    
    tab1, tab2 = st.tabs(["📊 Tabla de Métricas (RMSE/MAE)", "💡 Diagnóstico del Modelo"])
    
    with tab1:
        st.write("### Resultados Comparativos")
        st.dataframe(
            df_metrics.style.highlight_min(subset=['RMSE', 'MAE'], color='lightgreen', axis=0),
            use_container_width=True
        )
        
    with tab2:
        st.write("### Lectura Económica")
        st.info(
            "**Superioridad del GBM:** El modelo de Gradient Boosting superó ampliamente "
            "al Transformer en activos de larga duración (TLT, IEF), logrando un RMSE significativamente "
            "menor (ej. 0.025 vs 0.421 en TLT_Q1)."
        )
        st.warning(
            "**Diagnóstico Deep Learning:** Los altos márgenes de error en el Transformer "
            "sugieren problemas de overfitting por el tamaño de la ventana OOS o inestabilidad en los gradientes. "
            "Requiere ajuste de hiperparámetros (Dropout, Weight Decay)."
        )

except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'comparison_baselines.csv'. Asegúrate de ejecutar el pipeline de evaluación de la S9.")
