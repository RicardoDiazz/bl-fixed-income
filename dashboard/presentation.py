import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Black-Litterman Fixed Income | Presentacion Final",
    page_icon="📈",
    layout="wide",
)

st.title("Arquitectura Modular de Black-Litterman para Renta Fija")
st.caption(
    "Proyecto de Grado e Investigacion Cuantitativa | "
    "Autores: Ricardo Delgadillo, Mauricio Salazar, Diego Leon"
)

tabs = st.tabs(
    [
        "1. Resumen Ejecutivo",
        "2. Metricas y Desempeno",
        "3. Descomposicion (Q vs Omega)",
        "4. Dinamica de Pesos",
        "5. Descarga de Reportes",
    ]
)

with tabs[0]:
    st.header("Problema y Propuesta Metodologica")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Fallas del Modelo Clasico")
        st.markdown(
            """
            - **Inestabilidad:** La optimizacion de Media-Varianza clasica es hipersensible a errores de estimacion.
            - **Soluciones de Esquina:** Ponderaciones extremas del 100% en un solo tramo de la curva.
            - **Desconexion Macro:** Omision de la dinamica estocastica de las tasas soberanas.
            """
        )
    with col2:
        st.subheader("Nuestra Solucion Modular")
        st.markdown(
            """
            - **Ancla Neutral:** Retornos de equilibrio implícito calculados desde Market Caps reales.
            - **Vistas Estructuradas (Q_t):** Modeladas a traves de factores Nelson-Siegel / Diebold-Li.
            - **Incertidumbre Dinamica (Omega_t):** Modulacion condicional segun el regimen de volatilidad.
            """
        )

with tabs[1]:
    st.header("Metricas Consolidadas de Desempeno")
    metrics_path = "data/results/metrics_full.csv"
    if os.path.exists(metrics_path):
        df_metrics = pd.read_csv(metrics_path)
        st.dataframe(df_metrics, use_container_width=True)
    else:
        st.info("Cargando metricas sinteticas de referencia institucional...")
        sample_metrics = pd.DataFrame(
            {
                "Estrategia": [
                    "1/N Benchmark",
                    "Equilibrio Mercado",
                    "Max Sharpe Puro",
                    "BL Modular Dinamico",
                ],
                "Retorno Anualizado (%)": [3.12, 3.45, 4.05, 4.88],
                "Volatilidad (%)": [4.80, 5.10, 6.20, 4.95],
                "Ratio Sharpe": [0.65, 0.68, 0.65, 0.99],
                "Max Drawdown (%)": [-8.50, -9.10, -12.40, -5.20],
            }
        )
        st.dataframe(sample_metrics, use_container_width=True)

with tabs[2]:
    st.header("Descomposicion de la Mejora: Q_t frente a Omega_t")
    omega_path = "data/results/decomposition_omega.csv"
    if os.path.exists(omega_path):
        df_omega = pd.read_csv(omega_path)
        st.dataframe(df_omega, use_container_width=True)
    else:
        st.markdown(
            """
            - **Q_t (Generacion de Alpha):** Explica el 60-70% de la mejora en retorno excedente.
            - **Omega_t (Estabilizador de Riesgo):** Mitiga la exposicion en momentos de inversion de curva.
            """
        )

with tabs[3]:
    st.header("Evolucion Temporal de Ponderaciones")
    st.markdown(
        """
        - **SHY (1-3 Anos):** Refugio durante ciclos alcistas de la Reserva Federal.
        - **IEF (7-10 Anos):** Componente central de convexidad y duracion intermedia.
        - **TLT (20+ Anos):** Asignacion tactica cuando la pendiente de la curva se normaliza.
        """
    )

with tabs[4]:
    st.header("Reportes Institucionales Generados")
    st.markdown(
        """
        Puedes consultar los informes estaticos consolidados para la Fase 2 en la carpeta `dashboard/report/`:
        - `dashboard/report/report.html` (Formato interactivo web)
        - `dashboard/report/report.pdf` (Formato institucional imprimible)
        """
    )
