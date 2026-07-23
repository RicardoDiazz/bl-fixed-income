import numpy as np
import yfinance as yf


def download_fixed_income_data(tickers=None, period="5y"):
    if tickers is None:
        tickers = ["SHY", "IEF", "TLT"]    
    """
    Descarga datos historicos de ETFs de bonos del tesoro y calcula rendimientos.
    """
    print(f"Descargando datos para: {tickers}...")
    # Descargamos todo el DataFrame
    df = yf.download(tickers, period=period)

    # Seleccionamos Adj Close de forma segura manejando el MultiIndex
    if "Adj Close" in df.columns.levels[0]:
        data = df["Adj Close"]
    else:
        data = df["Close"]  # Por si acaso en algunas configuraciones cambia

    # Limpiar datos nulos
    data = data.dropna()

    # Calcular rendimientos logaritmicos diarios
    returns = np.log(data / data.shift(1)).dropna()

    return data, returns


if __name__ == "__main__":
    prices, returns = download_fixed_income_data()
    print("\n--- Precios (Ultimos registros) ---")
    print(prices.tail())
    print("\n--- Rendimientos Diarios (Ultimos registros) ---")
    print(returns.tail())
