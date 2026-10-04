# Analisis Economico por Regimenes de Mercado (S16)

Este documento examina el desempeno condicional de las estrategias de asignacion Black-Litterman frente a los portafolios de referencia a traves de distintos regimenes de tasas de interes y ciclos macroeconomicos.

## 1. Caracterizacion de los Regimenes de Mercado

La muestra historica de evaluacion fuera de muestra abarca escenarios de alta heterogeneidad macroeconomica:

1. **Regimen de Politica Monetaria Restrictiva (Ciclo Alcista):** 
   - Periodo caracterizado por incrementos acelerados en la tasa de fondos federales por parte de la Reserva Federal.
   - Presion a la baja sobre las valoraciones de bonos del tesoro soberanos, afectando severamente al tramo largo de la curva debido a su mayor duracion efectiva.
2. **Regimen de Aplanamiento e Inversion de Curva:**
   - La pendiente (diferencial 10Y-2Y / 10Y-3M) colapsa hacia terreno negativo.
   - Las visiones lineales estaticas tienden a subestimar el riesgo de duracion, mientras que la adaptacion dinamica protege el capital.
3. **Regimen de Normalizacion o Flexibilizacion:**
   - Recuperacion de pendiente positiva con desempeno favorable en tramos intermedios y largos.

## 2. Desempeno Relativo de las Estrategias por Regimen

- **Portafolio Equitativo (1/N) y Equilibrio de Mercado:**
  - Exhiben vulnerabilidad estructural en ciclos de endurecimiento monetario por mantener ponderaciones pasivas en tramos de alta duracion (TLT).
- **Estrategias Black-Litterman con Vistas Predictivas (BL_ML):**
  - Ajustan dinamicamente las exposiciones hacia el tramo corto (SHY) cuando los pronosticos anticipan presiones alcistas en rendimiento.
  - Mitigan caidas maximas (Max Drawdown) durante episodios de inversion de curva mediante una contraccion oportuna de la duracion del portafolio.

## 3. Conclusiones Metodologicas
La resiliencia de la arquitectura Black-Litterman no radica unicamente en la seleccion del pronostico puntual, sino en su capacidad para reponderar la convexidad y duracion de la cartera segun el regimen imperante.
