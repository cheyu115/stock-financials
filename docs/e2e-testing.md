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

## 核心計算邏輯

- 使用 pytest 撰寫 stock.py 中 calculate_pe_ratio 和 calculate_peg_ratio 的測試，包含 happy path, sad path, edge case

## 新增 github action CI

- 在每一次 push 和 merge 時安裝環境和執行 pytest

## Refine

- API 的錯誤處理產生了變更，確認 api 和 yfinance_fetcher 的實作。更新現有的 test_api 模組，並告知我新版本如何對齊實作
- pytest 對 API 的測試被限有的限流策略阻擋，講解原因和解決方案
- test_api 會失敗。因為 data/history.db 是在 docker 服務啟動時建立的，所以 local 沒有權限。因為這個檔案的 owner 是 root。讓 api 在測試的時候去建立和讀取另一個資料庫