# 1. 使用官方 Python 3.13 輕量版
FROM python:3.13-slim

# 2. 從官方 uv 映像檔複製執行檔，這是目前最快的安裝方式
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. 設定容器內的工作目錄
WORKDIR /app

# 4. 複製依賴宣告檔案
COPY pyproject.toml uv.lock ./

# 5. 安裝依賴 (不安裝開發測試工具，確保環境純淨)
RUN uv sync --frozen --no-dev

# 6. 複製專案原始碼與靜態檔案
COPY . .

# 7. 建立 SQLite 存放資料的目錄
RUN mkdir -p /app/data

# 8. 暴露 FastAPI 埠號
EXPOSE 8000

# 9. 啟動服務 (注意：必須綁定 0.0.0.0 才能讓容器外訪問)
CMD ["uv", "run", "uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]