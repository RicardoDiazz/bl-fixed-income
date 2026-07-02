import os

import pandas as pd
import yfinance as yf


def download_financial_data():
    """Descarga datos históricos de los ETFs SHY, IEF y TLT desde Yahoo Finance."""
    tickers = ["SHY", "IEF", "TLT"]
    print(f"Iniciando la descarga de activos: {tickers}")

    os.makedirs("data/raw", exist_ok=True)

    try:
        # Descargamos los datos de forma explícita grupal
        df = yf.download(tickers, start="2010-01-01", group_by="ticker", progress=False)

        if df.empty:
            raise ValueError(
                "No se obtuvieron datos. Revisa la conexión o los tickers."
            )

        # Extraemos el precio de cierre ajustado para cada ticker de forma segura
        datos_list = []
        for ticker in tickers:
            if ticker in df.columns.levels[0]:
                # Buscamos la columna de cierre ajustado que a veces se llama 'Adj Close' o 'Close'
                columna_cierre = (
                    "Adj Close" if "Adj Close" in df[ticker].columns else "Close"
                )
                serie_ticker = df[ticker][columna_cierre].rename(ticker)
                datos_list.append(serie_ticker)

        # Concatenamos todos los tickers en un solo DataFrame estructurado
        df_close = pd.concat(datos_list, axis=1)

        # Guardar archivo crudo
        raw_path = "data/raw/precios_crudos.csv"
        df_close.to_csv(raw_path)
        print(f"¡Descarga exitosa! Datos guardados correctamente en: {raw_path}")

    except Exception as e:
        print(f"Error crítico durante la descarga de datos: {e}")
        raise


if __name__ == "__main__":
    download_financial_data()
