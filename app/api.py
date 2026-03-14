from fastapi import FastAPI, HTTPException

# 引入我們已經寫好的模組
from app.yfinance_fetcher import fetch_stock_data
from app.stock import create_stock_record
from app.database import save_to_db

# 建立 FastAPI 實例
app = FastAPI(title="Stock Financials API")


@app.get("/stock/{ticker}")
def get_stock_info(ticker: str) -> dict:
    """
    Fetch stock data, calculate financial ratios, and save to the database.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        dict: JSON schema containing symbol, price, eps, pe, growth, and peg.

    Raises:
        HTTPException: 404 error if the ticker cannot be found.
    """
    # 1. extract parameter (統一轉大寫以符合格式)
    symbol = ticker.upper()

    # 2. call `fetch_stock_data`, handle success/failure cases
    stock_data = fetch_stock_data(symbol)
    if not stock_data:
        raise HTTPException(status_code=404, detail=f"Failed to find ticker: {symbol}")

    # 3. create StockStatistics record
    record = create_stock_record(ticker, stock_data)
    save_to_db(record)

    # 4. return json data
    return {
        "symbol": record.ticker,
        "price": record.price,
        "eps": record.eps,
        "pe": record.pe_ratio,
        "growth": record.eps_growth,
        "peg": record.peg_ratio,
    }
