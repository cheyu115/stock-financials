import datetime
from fastapi import FastAPI, HTTPException

# 引入我們已經寫好的模組
from app.yfinance_fetcher import fetch_stock_data
from app.stock import StockStatistics, calculate_pe_ratio, calculate_peg_ratio
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

    # 3. calculate PE and PEG ratios
    pe = calculate_pe_ratio(stock_data.price, stock_data.eps)
    peg = calculate_peg_ratio(pe, stock_data.eps_growth)

    # 4. save result to database
    today_str = str(datetime.date.today())
    record = StockStatistics(
        ticker=symbol,
        price=stock_data.price,
        eps=stock_data.eps,
        eps_growth=stock_data.eps_growth,
        pe_ratio=pe,
        peg_ratio=peg,
        date=today_str,
    )
    save_to_db(record)

    # 5. return json data
    return {
        "symbol": symbol,
        "price": stock_data.price,
        "eps": stock_data.eps,
        "pe": pe,
        "growth": stock_data.eps_growth,
        "peg": peg,
    }
