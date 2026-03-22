import logging
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.database import init_db, save_to_db
from app.stock import create_stock_record

# 引入我們已經寫好的模組
from app.yfinance_fetcher import fetch_stock_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --- 改用現代的 lifespan 取代 on_event ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """伺服器啟動時，確保資料夾存在並初始化資料庫"""
    init_db()
    yield  # 交出控制權讓應用程式運行


# 建立 FastAPI 實例，並綁定 lifespan
app = FastAPI(title="Stock Financials API", lifespan=lifespan)


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


def verify_client_and_rate_limit(request: Request) -> None:
    """
    可重複使用的防爬蟲與限流依賴 (Dependency)
    """
    # 1. 取得真實 IP
    client_ip = request.headers.get("X-Forwarded-For")
    if not client_ip:
        client_ip = request.client.host if request.client else "127.0.0.1"
    else:
        client_ip = client_ip.split(",")[0].strip()

    # 2. 簡易防爬蟲
    user_agent = request.headers.get("user-agent", "").lower()
    if not user_agent or "python-requests" in user_agent or "curl" in user_agent:
        raise HTTPException(status_code=403, detail="Forbidden")

    # 3. 簡易限流邏輯
    current_time = time.time()
    last_request_time = ip_tracker.get(client_ip, 0)

    if current_time - last_request_time < COOLDOWN_SECONDS:
        raise HTTPException(
            status_code=429, detail="請求太頻繁，請稍後再試 (Too Many Requests)"
        )

    # 通過檢查
    ip_tracker[client_ip] = current_time


@app.get("/")
def serve_html():
    return FileResponse("index.html")


@app.get(
    "/stock/{ticker}",
    response_model=StockResponse,
    dependencies=[Depends(verify_client_and_rate_limit)],
)
def get_stock_info(ticker: str) -> StockResponse:
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
    try:
        stock_data = fetch_stock_data(symbol)
    except RuntimeError as e:
        # 使用 logging 紀錄底層拋出的 HTTP error 或 Runtime error
        error_msg = str(e)
        logger.error(f"抓取 {symbol} 股票資料失敗: {error_msg}")

        # 轉換成 HTTP 502 (Bad Gateway) 告訴前端遠端伺服器出錯
        raise HTTPException(status_code=502, detail=error_msg)

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
