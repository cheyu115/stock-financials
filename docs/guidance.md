# Basic Rules

1. 參考 `main.py`, `stock.py`, `utils.py`, 使用現代 python 風格，包含但不限於 type hinting, docstring 寫出可維護的程式碼。
2. 保持模組化的思維，依照需求建立新的檔案。
3. 使用 doctest 進行基本的測試與輸入防呆。

# Specs

1. 參考 `database.md` 的規格，完成資料儲存的功能
2. 參考 `yfinance.md` 的規格，完成透過 API 做資料的取得
3. 參考 `api.md` 的規格，實作 API endpoint
4. 參考 `frontend.md` 實作使用者介面

# Todos

### End-to-End testing
模仿使用者實際操作時的情況

### 資料快取
先查詢資料庫是否已經存在「當天日期+股票代碼」的紀錄，若有則直接回傳，沒有才查詢API

### API 安全
針對同一ip請求的rate limiting

### 環境變數
像是資料庫名稱和csv文件檔名應儲存在環境變數