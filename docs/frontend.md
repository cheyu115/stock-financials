建立一個網頁，透過 API 請求 FastAPI 後端。

## Tools

- Modern HTML5
- Vanilla Javascript
- Pico.css

## UI/UX

- 類似 Google 首頁的極簡風格
- 標題： Stock Financials
- 搜尋： 一個輸入框(Placeholder: 輸入股票代碼，如 AAPL) 和一個按鈕(Text: 查詢)
- 結果區域：顯示查詢結果的卡片

## 行為

- 搜尋後清除輸入
- 必須處理成功和失敗的情況

## 規則

- 只要寫在一個 index.html 檔案就好
- css 透過 cdn import

## API call

- 使用 vanilla javascript fetch
- 只需要使用 `@app.get("/stock/{ticker}", response_model=StockResponse)` 這個 endpoint

## Refine

1. 修正兩點：查詢和搜尋欄高度不一致，且佔用太多橫向空間，置中，限制寬度為網頁的一半，結果卡片也要做一樣的對齊
2. html上搜尋和查詢的form仍然佔滿整個螢幕寬度，修改為50%的寬度並置中
3.  當結果卡片產生後，置中的輸入表單會被往上推動。上調輸入表單或著讓下移結果卡片，我要讓這個表單固定在畫面上，不管有沒有結果卡片存在。 