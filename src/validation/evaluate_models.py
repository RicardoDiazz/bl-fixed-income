"""Script para evaluar y comparar los pronósticos OOS de todos los modelos."""

import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error

def evaluate_all_models():
    """Calcula métricas de error para Ridge, GBM, LSTM y Transformer, y exporta un CSV."""
    targets_path = "data/processed/panel_semanal.parquet"
    output_csv = "data/processed/comparison_baselines.csv"
    
    models = ["ridge", "gbm", "lstm", "transformer"]
    
    # 1. Cargar datos reales
    if not os.path.exists(targets_path):
        raise FileNotFoundError(f"No se encontró el archivo de targets: {targets_path}")
        
    y_full = pd.read_parquet(targets_path)
    target_cols = [col for col in y_full.columns if any(q in col for q in ["_Q1", "_Q2", "_Q3"])]
    y_true_all = y_full[target_cols].dropna()
    
    results = []
    
    # 2. Iterar sobre cada modelo y calcular métricas
    print("Evaluando modelos y calculando métricas OOS...\n")
    
    for model_name in models:
        pred_path = f"data/processed/forecasts_{model_name}.parquet"
        
        if not os.path.exists(pred_path):
            print(f"⚠️ Advertencia: No se encontró {pred_path}. Saltando...")
            continue
            
        preds = pd.read_parquet(pred_path)
        
        # Alinear fechas (índices) comunes
        common_idx = preds.index.intersection(y_true_all.index)
        y_true = y_true_all.loc[common_idx]
        y_pred = preds.loc[common_idx]
        
        for col in target_cols:
            if col in y_pred.columns:
                # FILTRO ANTI-INFINITOS:
                mask = np.isfinite(y_true[col]) & np.isfinite(y_pred[col])
                y_t_clean = y_true[col][mask]
                y_p_clean = y_pred[col][mask]
                
                if len(y_t_clean) == 0:
                    print(f"⚠️ Saltando {model_name} - {col} por exceso de infinitos/NaNs.")
                    continue

                rmse = np.sqrt(mean_squared_error(y_t_clean, y_p_clean))
                mae = mean_absolute_error(y_t_clean, y_p_clean)
                
                results.append({
                    "Model": model_name.upper(),
                    "Target": col,
                    "RMSE": round(rmse, 6),
                    "MAE": round(mae, 6),
                    "N_Periods": len(y_t_clean)
                })
                
    # 3. Exportar resultados
    df_results = pd.DataFrame(results)
    
    # Ordenar para que sea fácil comparar el mismo target entre modelos
    df_results = df_results.sort_values(by=["Target", "RMSE"])
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_results.to_csv(output_csv, index=False)
    
    print(df_results.to_string(index=False))
    print(f"\n✅ Resultados guardados exitosamente en: {output_csv}")

if __name__ == "__main__":
    evaluate_all_models()