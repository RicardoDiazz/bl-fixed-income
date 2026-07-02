\# Decisiones Técnicas y de Arquitectura de Datos - Semana 2



Este documento detalla las decisiones de diseño e ingeniería de software implementadas para el pipeline de extracción y procesamiento de datos del modelo Black-Litterman enfocado en renta fija (ETFs de Tesoros: SHY, IEF, TLT).



\## 1. Frecuencia de los Datos (Muestreo Semanal)

\* \*\*Decisión:\*\* Los datos diarios extraídos de Yahoo Finance se consolidaron a una frecuencia \*\*semanal (`W`)\*\*, tomando el último precio de cierre ajustado registrado en cada período.

\* \*\*Justificación Financiera:\*\* El ruido de alta frecuencia (diario) en el mercado de renta fija puede distorsionar las estimaciones de la matriz de covarianza y los retornos implícitos del equilibrio de Black-Litterman. La frecuencia semanal suaviza las anomalías de liquidez de corto plazo y se alinea mejor con los horizontes típicos de rebalanceo de portafolios institucionales.



\## 2. Tratamiento de Datos Faltantes y Limpieza

\* \*\*Cálculo de Retornos:\*\* Se calcularon retornos porcentuales simples mediante el método `.pct\_change()`, idóneos para la formulación clásica de optimización de portafolios de Markowitz y Black-Litterman.

\* \*\*Manejo de NaNs:\*\* La primera fila resultante del cálculo de retornos (que carece de un período previo de comparación) fue eliminada de forma estricta usando `.dropna()`. No se aplicaron métodos de imputación (como \*forward fill\* o \*backward fill\*) para evitar la inyección de autocorrelación artificial o sesgos de supervivencia en el histórico de los ETFs.



\## 3. Formato de Almacenamiento (Parquet vs. CSV)

\* \*\*Decisión:\*\* Los datos procesados se exportaron en formato \*\*Parquet\*\* (`panel\_semanal.parquet`) utilizando el motor `pyarrow`.

\* \*\*Justificación Técnica:\*\* \* \*\*Esquema e Integridad:\*\* A diferencia de un archivo CSV, Parquet preserva de forma nativa los tipos de datos (como el índice de tiempo `DatetimeIndex` y los flotantes de alta precisión).

&#x20; \* \*\*Rendimiento:\*\* Utiliza almacenamiento columnar y compresión eficiente, optimizando los tiempos de lectura y carga en memoria cuando el script de optimización matemática invoque el dataset.

