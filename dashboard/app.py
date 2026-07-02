import os
import plotly.express as px
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard EDA - Renta Fija", layout="wide")

st.title("📊 Dashboard de Análisis Exploratorio de Datos (EDA)")
st.caption("Fase de validación de variables predictivas y targets - Ricardo")

# Cargar datos congelados
data_path = "data/processed/features.parquet"

if not os.path.exists(data_path):
    st.error(f"No se encontró el archivo de características en {data_path}. Corre 'make features' primero.")
    st.stop()

df = pd.read_parquet(data_path)
assets = ["SHY", "IEF", "TLT"]

# --- MENÚ DE NAVEGACIÓN (5 SECCIONES FORMALES) ---
tabs = st.tabs([
    "1. Vista General del Dataset",
    "2. Histórico de Precios",
    "3. Análisis de Retornos",
    "4. Distribución de Targets",
    "5. Matriz de Características (Lags)"
])

# SECCIÓN 1: Vista General del Dataset
with tabs[0]:
    st.header("📋 Resumen Estructurado del Panel Semanal")
    st.write(f"**Total de Registros Semanales:** {df.shape[0]}")
    st.write(f"**Total de Variables Computadas:** {df.shape[1]}")
    st.dataframe(df.head(10), use_container_width=True)

# SECCIÓN 2: Histórico de Precios
with tabs[1]:
    st.header("📈 Evolución de los Precios de Cierre Ajustados")
    selected_asset = st.selectbox("Selecciona el ETF de Tesoro a analizar:", assets, key="price_asset")
    fig_price = px.line(df, y=selected_asset, title=f"Precio Histórico - {selected_asset}", labels={"value": "Precio USD", "index": "Fecha"})
    st.plotly_chart(fig_price, use_container_width=True)

# SECCIÓN 3: Análisis de Retornos
with tabs[2]:
    st.header("🔄 Retornos Logarítmicos Semanales")
    selected_ret = st.selectbox("Selecciona el ETF para ver sus retornos:", assets, key="ret_asset")
    fig_ret = px.line(df, y=f"{selected_ret}_ret", title=f"Volatilidad de Retornos Semanales - {selected_ret}", labels={"value": "Retorno Log", "index": "Fecha"})
    st.plotly_chart(fig_ret, use_container_width=True)

# SECCIÓN 4: Distribución de Targets
with tabs[3]:
    st.header("🎯 Análisis de Variables Objetivo (Q1, Q2, Q3)")
    target_asset = st.selectbox("Selecciona el Activo Objetivo:", assets, key="target_asset")
    horizon = st.radio("Horizonte de Predicción:", ["Q1 (1 Sem)", "Q2 (2 Sem)", "Q3 (4 Sem)"])
    
    horizon_code = horizon.split(" ")[0]
    target_col = f"{target_asset}_{horizon_code}"
    
    fig_hist = px.histogram(df, x=target_col, marginal="box", title=f"Distribución del Target: {target_col}", nbins=50, labels={target_col: "Retorno Futuro"})
    st.plotly_chart(fig_hist, use_container_width=True)

# SECCIÓN 5: Matriz de Características (Lags)
with tabs[4]:
    st.header("⚙️ Inspección de Variables Rezagadas (Lags)")
    st.markdown("Verificación visual de las variables de entrada construidas para alimentar el modelo predictivo:")
    
    lag_cols = [col for col in df.columns if "_lag_" in col]
    if lag_cols:
        st.dataframe(df[lag_cols].describe(), use_container_width=True)
    else:
        st.warning("No se encontraron variables con rezago en el archivo.")