# Stock Financials API

使用 FastAPI 實作的服務，抓取股票數據、計算財務指標（PE/PEG）並儲存至 SQLite 資料庫。

**Live Demo:** [https://stock-financials-pzv1.onrender.com/](https://stock-financials-pzv1.onrender.com/)

## Tools

- 語言與環境: Python 3.13, uv
- 後端框架: FastAPI, Uvicorn
- 測試工具: pytest, unittest.mock
- 資料處理: yfinance, sqlite3

## Practice

我關注可維護性與基礎工程習慣：

- 模組化: 拆分系統為資料獲取 (`yfinance_fetcher.py`)、邏輯計算 (`stock.py`)、資料庫操作 (`database.py`) 與 API 路由 (`api.py`)
- 現代 Python: 使用 Type Hinting 和 Dataclass 提高可讀性，使用 `pathlib` 處理路徑
- 減少重複代碼: 將資料組裝與 PE/PEG 計算取出成獨立的 `create_stock_record` ，讓 CLI 與 API 共用邏輯
- 單元測試: 撰寫測試時使用 `@patch` 攔截 `yfinance` 的外部請求，注入 Mock 假資料，確保測試結果能穩定重現

## How I use AI

我寫「規格和系統邊界」，並由 AI「審查與實作」

1. 先寫規格: 先寫 Markdown (`docs/api.md`, `docs/yfinance.md`) 定義好 Input/Output 格式和行為
2. 上下文約束: 提供明確的 JSON Schema、型別限制與錯誤處理情境（如 404 Not Found），降低 AI 產生幻覺 (Hallucination) 的機率。
3. 系統設計: 我設計資料模型，以及系統間的溝通方式(yfinance API、資料庫、JSON)，再使用 AI 產生實作。

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

啟動後可至以下網址進行測試：

- 前端 UI 介面: http://127.0.0.1:8000/
- 後端 API (Swagger): http://127.0.0.1:8000/docs