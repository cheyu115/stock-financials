使用 Playwright 撰寫 End-to-End Testing

## 設定

- HTML是 `index.html`
- API是 `app/api.py`

## 首頁載入

- GET /
- 應該有標題，輸入表單，查訊按鈕

## 使用者輸入與查詢成功

- GET /stock/{ticker}
- 模擬使用者輸入並發送，使用 Mock 模擬 API 查詢結果成功

## 使用者輸入與查詢失敗

- GET /stock/{ticker}
- 模擬使用者輸入並發送，使用 Mock 模擬 API 查詢結果失敗