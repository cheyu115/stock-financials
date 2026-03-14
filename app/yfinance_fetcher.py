from dataclasses import dataclass
from typing import Optional

import yfinance as yf


@dataclass
class YfinanceData:
    """
    從 yfinance 取得的股票統計資料結構
    """

    price: float
    eps: float
    eps_growth: float


def fetch_stock_data(ticker_symbol: str) -> Optional[YfinanceData]:
    """
    透過 yfinance 取得股票的即時報價、EPS 與明年的預估成長率。

    Args:
        ticker_symbol (str): 股票代碼 (例如 'AAPL')

    Returns:
        YfinanceData | None: 若成功取得報價則回傳資料物件，若無法取得報價或發生錯誤則回傳 None。

    >>> # 測試防呆機制 (模擬一個不存在的股票代碼)
    >>> fetch_stock_data("INVALID_TICKER_12345") is None
    True
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
    except Exception:
        # 捕捉網路斷線或 yfinance 套件本身的 Exception
        return None

    # 1. 取得目前報價 (若無 currentPrice，嘗試 previousClose)
    price = info.get("currentPrice") or info.get("previousClose")

    # 錯誤處理 1: 如果抓取不到 price 的資料，返回 None (根據 yfinance.md 規格)
    if not price:
        return None

    # 2. 取得 EPS
    # 錯誤處理 2: 如果抓取不到 EPS，預設填入 0
    eps = info.get("trailingEps") or 0.0

    # 3. 取得 Next Year Growth Estimate (Analysis 分頁)
    eps_growth = 0.0
    try:
        # 使用 earnings_estimate 表格，其 index 為 ['0q', '+1q', '0y', '+1y']
        # 我們取 '+1y' (Next Year) 的 'growth' 欄位
        ee = stock.earnings_estimate
        if ee is not None and not ee.empty and "+1y" in ee.index:
            # yfinance 通常回傳小數 (例如 0.157 代表 15.7%)
            val = ee.loc["+1y", "growth"]
            # 規格要求：15% 儲存為 15
            if isinstance(val, (int, float)):
                eps_growth = float(val) * 100.0 if val else 0.0
    except Exception:
        # 如果 Analysis 表格抓取失敗，保持為 0.0
        pass

    return YfinanceData(
        price=round(float(price), 2),
        eps=round(float(eps), 2),
        eps_growth=round(float(eps_growth), 2),
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
