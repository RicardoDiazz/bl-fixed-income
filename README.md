======================================================================

PIPELINE PREDICTIVO DE MACHINE LEARNING PARA RENTA FIJA (US TREASURIES)

======================================================================



Este repositorio contiene una implementacion profesional, modular y

automatizada de un pipeline de Machine Learning orientado a series de

tiempo financieras. El objetivo principal es predecir los retornos

futuros en multiples horizontes temporales utilizando activos de renta

fixa (ETFs de bonos del tesoro de EE. UU.: SHY, IEF, TLT).



El proyecto gestiona de extremo a extremo la ingesta de datos, el

control de calidad, el analisis econometrico de estacionariedad, la

ingenieria de variables sin sesgo temporal (anti data-leakage) y la

visualizacion interactiva para el analisis exploratorio de datos.





\----------------------------------------------------------------------

\----------------------------------------------------------------------



El repositorio se encuentra estructurado bajo los siguientes modulos de

codigo de produccion e informes tecnicos institucionales:



\- src/data/download.py

&#x20; Módulo de ingesta automatizada. Descarga precios historicos de cierre

&#x20; ajustados directos desde la API de Yahoo Finance.



\- src/data/clean.py

&#x20; Módulo de preprocesamiento. Sincroniza las fechas del panel, maneja

&#x20; dias feriados del mercado y ejecuta la imputacion de valores nulos.



\- src/features/returns.py

&#x20; Módulo de transformacion. Convierte las series de precios continuas

&#x20; en retornos logaritmicos semanales estabilizados.



\- src/features/targets.py

&#x20; Módulo de variables objetivo. Construye los targets predictivos a

&#x20; futuro para los horizontes Q1 (1 semana), Q2 (2 semanas) y Q3 (4 semanas).



\- src/features/build\_features.py

&#x20; Módulo de ingenieria de variables. Computa rezagos historicos (lags

&#x20; 1, 2 y 3) para cada ETF y congela la matriz final para el modelo.



\- dashboard/app.py

&#x20; Aplicacion web interactiva desarrollada en Streamlit. Provee el

&#x20; Analisis Exploratorio de Datos (EDA) en 5 secciones completas.



\- tests/

&#x20; Suite de pruebas de control de calidad del software:

&#x20; \* test\_data.py: Validacion de la correcta ingesta y limpieza de datos.

&#x20; \* test\_targets.py: Verificacion de dimensiones y calculo de targets.

&#x20; \* test\_leakage.py: Prueba matematica estricta contra la filtracion temporal.



\- configs/

&#x20; Informes tecnicos de soporte metodologico para los evaluadores:

&#x20; \* data\_decisions.md: Justificacion de la frecuencia y limpieza de datos.

&#x20; \* targets\_analysis.md: Reporte del Test ADF con p-values de 0.0000.





\----------------------------------------------------------------------

2\. FUNDAMENTOS Y VALIDACIONES CIENTIFICAS

\----------------------------------------------------------------------



\- Estacionariedad (Test ADF):

&#x20; Todas las variables objetivo (Q1, Q2, Q3) de los tres activos fueron

&#x20; validadas mediante la prueba Aumentada de Dickey-Fuller (ADF) en

&#x20; src/features/targets.py. Se garantizo estadisticamente la ausencia

&#x20; de raices unitarias (p-value = 0.0000 < 0.05) para asegurar un

&#x20; entrenamiento convergente y estable en modelos de Machine Learning.



\- Mitigacion de Data Leakage:

&#x20; Se implemento un riguroso test posicional unitario en

&#x20; tests/test\_leakage.py empleando indexacion entera (.iloc). Este test

&#x20; verifica de forma automatizada en el CI/CD que el lag\_1 en el periodo

&#x20; actual t sea exactamente igual al retorno original en t-1, garantizando

&#x20; que los algoritmos no consuman informacion del futuro al entrenarse.





\----------------------------------------------------------------------

3\. INSTALACION Y REQUISITOS DE EJECUCION

\----------------------------------------------------------------------



El entorno utiliza 'uv' como gestor avanzado de dependencias para

asegurar la reproducibilidad del entorno virtual.



1\. Instalar y Sincronizar Dependencias del Proyecto:

&#x20;  .\\uv sync



2\. Ejecutar la Suite Completa de Pruebas Unitarias de Validacion:

&#x20;  .\\uv run pytest



3\. Compilar y Desplegar todo el Pipeline de Datos y Features:

&#x20;  make features



4\. Lanzar el Dashboard Interactivo de Analisis Exploratorio (EDA):

&#x20;  make eda



\- Validacion Cruzada y Protocolo Rolling (S6):

&#x20; Se implemento y congelo el protocolo de validacion temporal Expanding Window en

&#x20; src/models/rolling.py junto con el modulo de metricas cuantitativas (RMSE, MAE, MAPE)

&#x20; en src/models/metrics.py. Se garantizo mediante pruebas unitarias en

&#x20; tests/test\_rolling.py la correcta expansion del conjunto de entrenamiento sin

&#x20; traslape temporal ni fugas de informacion fuera de muestra (out-of-sample).



\- Modelos Baseline de Prediccion de Cuantiles (S7):

&#x20; Se implementaron los pipelines basales para la prediccion out-of-sample de los cuantiles de retorno (SHY, IEF, TLT). Se integro el modelo Ridge Regression en src/models/ridge.py y src/models/generate\_ridge\_forecasts.py, junto con una arquitectura de red neuronal recurrente LSTM en PyTorch (src/models/lstm.py y src/models/generate\_lstm\_forecasts.py). Se validaron mediante pruebas unitarias en tests/test\_lstm.py y se generaron las matrices alineadas de pronosticos en data/processed/forecasts\_ridge.parquet y data/processed/forecasts\_lstm.parquet.



\- Modelos No Lineales y Avanzados de Prediccion (S8):

&#x20; Se implementaron los pipelines avanzados para la prediccion out-of-sample incorporando arquitecturas no lineales. Se integro el modelo Gradient Boosting (LightGBM) en src/models/gbm.py y src/models/generate\_gbm\_forecasts.py, junto con una arquitectura de atencion Transformer en PyTorch (src/models/transformer.py y src/models/generate\_transformer\_forecasts.py). Se validaron mediante pruebas unitarias en tests/test\_gbm.py y tests/test\_transformer.py, y se generaron las matrices alineadas de pronosticos en data/processed/forecasts\_gbm.parquet y data/processed/forecasts\_transformer.parquet.

