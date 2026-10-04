# Analisis de Dinamica de Ponderaciones y Rotacion de Cartera (S16)

Este documento examina las caracteristicas de las asignaciones de pesos generadas por las estrategias Black-Litterman y los benchmarks tradicionales en el universo de bonos del tesoro de EE. UU. (SHY, IEF, TLT).

## 1. Estabilidad de los Pesos y Suavidad Temporal

Uno de los problemas clasicos de la optimizacion de media-varianza no restringida es la inestabilidad de las ponderaciones frente a pequenos cambios en los rendimientos esperados.
- **Enfoque Black-Litterman Modular:**
  - Al anclar la distribucion inicial en el equilibrio de mercado (Pi), la transicion de pesos entre semanas muestra una evolucion suave y gradual.
  - La matriz Omega_t previene saltos abruptos o asignaciones del 100% en un solo activo (soluciones de esquina), conservando la diversificacion estructural a lo largo de la curva soberana.

## 2. Rotacion de Cartera (Turnover) y Costos de Friccion

- **Benchmark 1/N y Mercado:** Rotacion minima orientada exclusivamente al rebalanceo pasivo.
- **Modelos de Retorno Puro (Momentum / Lineales no regularizados):** Tienden a generar una rotacion elevada, erosionando el exceso de retorno una vez deducidos los costos de transaccion.
- **Portafolios BL con Regularizacion:**
  - Mantienen un nivel de turnover controlado (inferior al 15% semanal en promedio).
  - La preservacion de alpha despues de deducir costos de transaccion (1-5 bps en el mercado de Treasuries liquidos) valida la viabilidad operativa institucional de la estrategia.

## 3. Gestion Dinamica de la Duracion

La ponderacion activa entre SHY (1-3 anos), IEF (7-10 anos) y TLT (20+ anos) actua como un mecanismo de ajuste dinamico de la duracion de cartera:
- Durante escenarios de elevacion de tasas, el modelo contrae la ponderacion de TLT e incrementa la exposicion en SHY, protegiendo el valor liquidativo.
- En fases de distension monetaria o aplanamiento estabilizado, expande la participacion en IEF y TLT para capturar convexidad y rendimiento corriente.
