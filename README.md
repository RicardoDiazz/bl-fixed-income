# Modelo Black-Litterman Aplicado a Renta Fija (Treasuries)

Este repositorio contiene una implementación profesional, modular y dinámica del **Modelo Black-Litterman** aplicado a activos de renta fija (ETFs de bonos del tesoro de EE. UU.: SHY, IEF, TLT). 

El proyecto automatiza la descarga de datos históricos reales de mercado, calcula el equilibrio implícito a través de la optimización inversa y ajusta los rendimientos esperados del mercado combinándolos matemáticamente con las opiniones subjetivas del analista (vistas). Finalmente, resuelve la asignación óptima de activos utilizando una optimización de Media-Varianza para maximizar el Ratio de Sharpe.

## 🚀 Estructura del Proyecto

* src/bl_fixed_income/data_loader.py: Extracción de datos históricos de Yahoo Finance.
* src/bl_fixed_income/analytics.py: Motor matemático y fórmulas de Black-Litterman.
* src/bl_fixed_income/allocator.py: Optimizador numérico de portafolios (Max Sharpe).
* src/bl_fixed_income/main.py: Pipeline principal y punto de ejecución dinámico.
* settings.toml: Centro de control dinámico del portafolio.

## 🧠 Fundamentos Matemáticos

El modelo combina la información del mercado con las vistas del analista usando las siguientes fórmulas matriciales:

1. Rendimientos Implícitos de Equilibrio
   Pi = delta * Sigma * w_mkt

2. Fórmula Maestra de Black-Litterman
   mu_bl = [ (tau * Sigma)^-1 + P^T * Omega^-1 * P ]^-1 * [ (tau * Sigma)^-1 * Pi + P^T * Omega^-1 * Q ]

## ⚙️ Configuración Dinámica (settings.toml)

Toda la configuración del modelo se gestiona de forma centralizada en el archivo settings.toml, donde puedes cambiar los tickers, el periodo de análisis, la tasa libre de riesgo y tus matrices de opiniones (P, Q, Omega) sin tocar el código de los scripts.

## 💻 Requisitos e Instalación

1. Instalar y Sincronizar Dependencias:
   .\uv sync

2. Ejecutar Pruebas de Consistencia:
   $env:PYTHONPATH = "src"; .\uv run pytest

3. Ejecutar el Modelo y Exportar Reportes:
   $env:PYTHONPATH = "src"; .\uv run python src/bl_fixed_income/main.py

Al finalizar la ejecución, el script guardará en la raíz del proyecto un gráfico de barras de alta resolución llamado portfolio_comparison.png.