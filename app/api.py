import os
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.database import BASE_DIR, init_db, save_to_db  # 新增引入 init_db 和 BASE_DIR
from app.stock import create_stock_record

# 引入我們已經寫好的模組
from app.yfinance_fetcher import fetch_stock_data

# 建立 FastAPI 實例
app = FastAPI(title="Stock Financials API")


@app.on_event("startup")
def startup_event():
    """伺服器啟動時，確保資料夾存在並初始化資料庫"""
    data_dir = BASE_DIR / "data"
    # 如果 data 資料夾不存在，就建立它 (包含父資料夾)
    os.makedirs(data_dir, exist_ok=True)
    # 初始化資料庫表格
    init_db()


class StockResponse(BaseModel):
    symbol: str
    price: float
    eps: float
    pe: float
    growth: float
    peg: float


# --- Workaround: 簡易 IP 請求紀錄器 ---
ip_tracker = {}
COOLDOWN_SECONDS = 3  # 限制同一個 IP 每 3 秒只能打一次 API


@app.get("/")
def serve_html():
    return FileResponse("index.html")


@app.get("/stock/{ticker}", response_model=StockResponse)
def get_stock_info(request: Request, ticker: str) -> StockResponse:
    """
    Fetch stock data, calculate financial ratios, and save to the database.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        dict: JSON schema containing symbol, price, eps, pe, growth, and peg.

    Raises:
        HTTPException: 404 error if the ticker cannot be found.
    """
    # BEGIN RATELIMITING WORKAROUND
    # 1. 取得真實 IP (因為部署在 Render 上，必須讀取 X-Forwarded-For Header)
    # 1. 取得真實 IP 的安全寫法
    client_ip = request.headers.get("X-Forwarded-For")
    if not client_ip:
        # 如果 request.client 存在就取 host，否則給一個預設值 "127.0.0.1"
        client_ip = request.client.host if request.client else "127.0.0.1"
    else:
        # X-Forwarded-For 有時候會是一串 IP (例如 "ip1, ip2")，我們取第一個最原始的 IP
        client_ip = client_ip.split(",")[0].strip()

    # --- 簡易防爬蟲 (擋掉沒有 User-Agent 的笨腳本) ---
    user_agent = request.headers.get("user-agent", "").lower()
    if not user_agent or "python-requests" in user_agent or "curl" in user_agent:
        raise HTTPException(status_code=403, detail="Forbidden")

    # --- 簡易限流邏輯 ---
    current_time = time.time()
    last_request_time = ip_tracker.get(client_ip, 0)

    if current_time - last_request_time < COOLDOWN_SECONDS:
        raise HTTPException(
            status_code=429, detail="請求太頻繁，請稍後再試 (Too Many Requests)"
        )
    # 通過檢查，更新該 IP 的請求時間
    ip_tracker[client_ip] = current_time
    # END RATELIMITING WORKAROUND

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
    return StockResponse(
        symbol=record.ticker,
        price=record.price,
        eps=record.eps,
        pe=record.pe_ratio,
        growth=record.eps_growth,
        peg=record.peg_ratio,
    )
