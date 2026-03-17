建立檔案 `yfinance_fetcher` 使用 yfinance 抓取統計資料。

# fetch_stock_data

1. 接受 ticker_symbol 字串為參數，並返回一個 dataclass
2. 資料包含目前的報價，EPS，以及明年的 Growth Estimates
3. Growth Estimate 假設是 15%，就儲存為15。不再轉換成小數。
4. 定義該 dataclass 為 YfinanceData

## Error Handling

1. 如果抓取不到 price 的資料，返回 None
2. 如果抓取不到 EPS 或 Growth Estimates，預設填入0

## Refine

1. 目前的程式碼在 `info.get('earningsGrowth') or 0.0` 抓取了 "Current Qtr. Growth Estimates"。我想要的是 "Next Year Growth Estimates"
2. 還是有落差，甚至錯誤更大了，這是Statistics分頁中的`Quarterly Earnings Growth  (yoy)`。我要的是Analysis分頁中的表格提供了 `Current Qtr., Next Qtr., Current Year, Next Year` 四欄中，我只要最右邊 Next Year 一欄
3. 在 yfinance_fetcher 中我們應該要清洗我們使用在 dataclass 中的資料，我只要保留小數點後兩位
4. 在 fetch_stock_data 這個 function 內，重構目前的錯誤處理。當網路錯誤或是 yfinance 套件本身出錯時，應該 raise 對應的 HTTP error 或是 error