\# Reporte de Decisiones de Datos



Este documento describe la procedencia, estructura y transformaciones aplicadas al set de datos del proyecto predictivo de renta fija.



\## 1. Fuentes de Información y Activos Seleccionados

Se seleccionaron tres ETFs de la familia de Tesoros de EE. UU. administrados por iShares para mapear tres tramos clave de la curva de rendimientos:

\- \*\*SHY (Short-Term):\*\* iShares 1-3 Year Treasury Bond ETF. Representa el tramo corto de la curva, altamente influenciado por las decisiones de tasas de interés de la Reserva Federal.

\- \*\*IEF (Intermediate-Term):\*\* iShares 7-10 Year Treasury Bond ETF. Representa el tramo medio de la curva, el cual captura expectativas de inflación y crecimiento económico a mediano plazo.

\- \*\*TLT (Long-Term):\*\* iShares 20+ Year Treasury Bond ETF. Representa el tramo largo de la curva, altamente sensible al riesgo de duración y primas por plazo a largo plazo.



La descarga de datos históricos se automatiza en `src/data/download.py` consumiendo los precios de cierre ajustados (`Adj Close`) a través de la API oficial de `yfinance`.



\## 2. Justificación de la Frecuencia Semanal

Se optó por una agregación y muestreo de frecuencia \*\*semanal (Weekly)\*\* debido a las siguientes razones metodológicas:

\- \*\*Reducción de Ruido:\*\* Los datos diarios de renta fija suelen incorporar ruido de microestructura de mercado (alta frecuencia, spreads de liquidez) que no aporta valor a las proyecciones macroeconómicas.

\- \*\*Estabilidad de Señal:\*\* Los movimientos en las tasas de interés y las primas de riesgo soberano responden a fundamentos que se consolidan de forma más limpia en horizontes semanales.

\- \*\*Evitar Overfitting:\*\* Disminuye el volumen de observaciones espurias, permitiendo que los modelos de Machine Learning generalicen mejor en horizontes futuros de mediano plazo (1 a 4 semanas).



\## 3. Tratamiento de Datos Faltantes (Nulos) y Limpieza

El proceso automatizado en `src/data/clean.py` implementa las siguientes reglas secuenciales de calidad:

1\. \*\*Alineación Temporal:\*\* Se remueven fechas que no cuenten con registros síncronos en los tres activos debido a días feriados específicos de los mercados.

2\. \*\*Imputación Directa:\*\* En caso de nulos transitorios, se aplica llenado hacia adelante (`ffill`) para mantener la continuidad del precio teórico del activo reflectante de la última información disponible.

3\. \*\*Consolidación de Parquet:\*\* El panel final limpio se exporta en formato indexado `data/processed/panel\_semanal.parquet` asegurando compresión y tipos de datos estrictos para el modelamiento.

