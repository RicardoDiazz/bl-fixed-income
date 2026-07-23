\# Análisis de Pronósticos y Diagnóstico de Modelos (Semana 9)



\## 1. Lectura Económica y Comparación de Modelos

A partir de la matriz de resultados OOS (Out-Of-Sample) consolidada en `comparison\_baselines.csv`, se observa una clara superioridad de los modelos basados en árboles (Gradient Boosting) sobre las arquitecturas de aprendizaje profundo puro en el corto plazo.



\*   \*\*Desempeño en Bonos de Larga Duración (TLT e IEF):\*\* El modelo LightGBM demostró una capacidad superior para capturar la varianza de los cuantiles de rendimiento. Para el cuantil inferior (`TLT\_Q1`), el GBM logró un RMSE de 0.0256 frente al 0.4218 del Transformer. Esto indica que las relaciones no lineales del mercado de renta fija a largo plazo fueron mejor abstraídas por la construcción iterativa de residuos del GBM.

\*   \*\*Curva Corta (SHY):\*\* Aunque la volatilidad en la parte corta de la curva suele estar anclada a las decisiones de política monetaria (lo que dificulta la predicción de ambos modelos), el Transformer logró un desempeño marginalmente mejor en el cuantil medio (`SHY\_Q2`), indicando cierta sensibilidad a secuencias temporales en activos de baja duración.



\## 2. Diagnóstico y Necesidades de Ajuste (Transformer / LSTM)

Los altos márgenes de error (RMSE y MAE) del Transformer, comparados con el baseline, evidencian un problema estructural en su aplicación actual:



1\.  \*\*Overfitting por Tamaño de Muestra:\*\* Las redes neuronales profundas (como la arquitectura de atención del Transformer) requieren volúmenes masivos de datos para evitar el sobreajuste. Con una ventana OOS pequeña, el modelo está perdiendo capacidad de generalización.

2\.  \*\*Explosión de Varianza:\*\* Los picos en las métricas de error sugieren que los gradientes del Transformer se desestabilizaron durante las ventanas rodantes. 



\### Siguientes Pasos (Tuning)

Para la fase final del proyecto, se proponen las siguientes acciones correctivas para los modelos profundos:

\*   Reducir el número de capas de atención (layers) para disminuir la complejidad del modelo.

\*   Aumentar los coeficientes de \*Dropout\* (ej. de 0.1 a 0.3) y aplicar \*Weight Decay\* estricto para forzar la regularización.

\*   Considerar estrategias de ensamblaje (Ensemble) donde los modelos profundos complementen, en lugar de competir, con las salidas del GBM.

