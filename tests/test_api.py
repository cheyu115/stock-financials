from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import app, verify_client_and_rate_limit
from app.yfinance_fetcher import YfinanceData

# 建立模擬瀏覽器發送請求的測試客戶端
client = TestClient(app)


# --- 新增這段：解除測試時的封印 ---
def skip_rate_limit():
    """假的限流函式，什麼都不做，直接放行"""
    pass


app.dependency_overrides[verify_client_and_rate_limit] = skip_rate_limit


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


@patch("app.api.fetch_stock_data")
def test_get_stock_bad_gateway(mock_fetch):
    """
    測試 502 Bad Gateway 失敗情況 (網路或套件錯誤)
    """
    # 模擬 fetch_stock_data 拋出 RuntimeError (而不是回傳值)
    error_msg = (
        "yfinance 套件發生內部錯誤: Too Many Requests. Rate limited. Try after a while."
    )
    mock_fetch.side_effect = RuntimeError(error_msg)

    response = client.get("/stock/AAPL")

    # 檢查 API 是否成功捕捉 RuntimeError 並轉換成 502
    assert response.status_code == 502
    assert response.json()["detail"] == error_msg
