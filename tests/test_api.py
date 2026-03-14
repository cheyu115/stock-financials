from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import app
from app.yfinance_fetcher import YfinanceData

# 建立模擬瀏覽器發送請求的測試客戶端
client = TestClient(app)


# 魔法在這裡：攔截 app.api 裡面的 fetch_stock_data 函式
@patch("app.api.fetch_stock_data")
def test_get_stock_success(mock_fetch):
    """
    測試 200 OK 成功情況
    """
    # 1. 設置 Mock 假資料：不管抓什麼，都固定回傳這包 YfinanceData
    mock_fetch.return_value = YfinanceData(price=200.0, eps=10.0, eps_growth=15.0)

    # 2. 模擬對 API 發送真實請求
    response = client.get("/stock/AAPL")

    # 3. 檢查結果是否與預期相符
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["price"] == 200.0
    assert data["pe"] == 20.0  # 200 / 10 = 20.0
    assert data["peg"] == 1.33  # 20 / 15 = 1.33


@patch("app.api.fetch_stock_data")
def test_get_stock_not_found(mock_fetch):
    """
    測試 404 Not Found 失敗情況
    """
    # 1. 設置 Mock 假資料：模擬 Yahoo Finance 找不到股票，回傳 None
    mock_fetch.return_value = None

    # 2. 模擬發送請求
    response = client.get("/stock/INVALID")

    # 3. 檢查是不是真的吐出 404 和正確的錯誤訊息
    assert response.status_code == 404
    assert response.json()["detail"] == "Failed to find ticker: INVALID"
