# Stock Financials API

使用 FastAPI 實作的服務，抓取股票數據、計算財務指標（PE/PEG）並儲存至 SQLite 資料庫。

## Practice

我關注可維護性與基礎工程習慣：

- 模組化: 拆分系統為資料獲取 (`yfinance_fetcher.py`)、邏輯計算 (`stock.py`)、資料庫操作 (`database.py`) 與 API 路由 (`api.py`)
- 現代 Python: 使用 Type Hinting 和 Dataclass 提高可讀性，使用 `pathlib` 處理路徑
- 減少重複代碼: 將資料組裝與 PE/PEG 計算取出成獨立的 `create_stock_record` ，讓 CLI 與 API 共用邏輯
- 單元測試: 撰寫測試時使用 `@patch` 攔截 `yfinance` 的外部請求，注入 Mock 假資料，確保測試結果能穩定重現
- 容器化: 使用 Dockerfile 與 docker-compose.yml 封裝執行環境

## How I use AI

我寫「規格和系統邊界」，並由 AI「審查與實作」。
AI使用文件直接產出第一版程式碼，每一次審查所發現的問題，修復的程式碼直接透過 **Refine** 下紀錄的 prompt logs 產出

1. 先寫規格: 在文件中 (`docs/api.md`, `docs/yfinance.md`) 定義好 Input/Output 格式和行為
2. 上下文約束: 提供明確的 JSON Schema、型別限制與錯誤處理情境（如 404 Not Found），降低 AI 產生幻覺 (Hallucination) 的機率。
3. 系統設計: 我設計資料模型，以及系統間的溝通方式(yfinance API、資料庫、JSON)，再使用 AI 產生實作。

## Roadmap

- End-to-End testing：模仿使用者實際操作時的情況

- 資料快取 (api)：先查詢資料庫是否已經存在「當天日期+股票代碼」的紀錄，若有則直接回傳，沒有才查詢API

- 更好的 API 安全 (api)：針對同一ip請求的rate limiting，使用slowapi 和 redis，或至少先在檔案做dict持久化。時間限制也應該做成 sliding window

## 啟動

1. 安裝依賴與環境
```bash
uv sync
```

2. 執行整合測試
```bash
uv run pytest
```

3. 啟動伺服器
```bash
uv run uvicorn app.api:app --reload
```

4. 使用 curl 測試
```bash
curl -H "User-Agent: Mozilla/5.0" http://127.0.0.1:8000/stock/aapl
```

## Docker

1. 建立 /data 資料夾
```bash
mkdir data
```

2. 啟動
```bash
docker compose up -d
```

啟動後可至以下網址進行測試：

- 前端 UI 介面: http://127.0.0.1:8000/
- 後端 API 文件 (Swagger): http://127.0.0.1:8000/docs

## Tools

- 語言與環境: Python 3.13, uv
- 後端框架: FastAPI, Uvicorn
- 測試工具: pytest, unittest.mock
- 資料處理: yfinance, sqlite3

## Live Demo

因為 `yfinance` 依賴爬蟲機制，查詢時有極高機率會觸發 Yahoo Finance 的 IP 封鎖導致查詢失敗。
```
yfinance 套件發生內部錯誤: Too Many Requests. Rate limited. Try after a while.
```
https://stock-financials-pzv1.onrender.com/