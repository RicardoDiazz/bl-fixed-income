import pytest
from bl_fixed_income.data_loader import download_fixed_income_data

def test_download_fixed_income_data():
    """
    Verifica que la descarga de datos de renta fija funcione,
    traiga los tickers correctos y calcule los rendimientos.
    """
    tickers = ["SHY", "IEF", "TLT"]
    prices, returns = download_fixed_income_data(tickers=tickers, period="1mo") # Periodo corto para el test
    
    # 1. Verificar que no esten vacios
    assert not prices.empty, "El DataFrame de precios esta vacio"
    assert not returns.empty, "El DataFrame de rendimientos esta vacio"
    
    # 2. Verificar que esten los tres activos esperados
    for ticker in tickers:
        assert ticker in prices.columns, f"Falta el ticker {ticker} en los precios"
        assert ticker in returns.columns, f"Falta el ticker {ticker} en los rendimientos"
