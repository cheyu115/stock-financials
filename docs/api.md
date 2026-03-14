使用 fastapi 建立 web 服務。

## data

### input

An HTTP request to endpoint
- Path parameter: `ticker` (string)
- No request body.

### output json schema
- symbol: string
- price: float
- eps: float
- pe: float
- growth: float (in percentage)
- peg: float

小數點要四捨五入到第二位 

## signature

- endpoint: `GET /stock/{ticker}`
- parameter: `ticker: string`

## example

### 200 OK

`GET /stock/aapl`

```json
{
  "symbol": "AAPL",
  "price": 185.92,
  "eps": 6.13,
  "pe": 30.33,
  "growth": 15.00,
  "peg": 2.02
}
```

### 404 Not Found

`GET /stock/INVALID_TICKER`

```json
{
    "detail": "Failed to find ticker: INVALID_TICKER"
}
```

## template

1. extract parameter
2. call `fetch_stock_data`, handle success/failure cases
3. calculate PE and PEG ratios
4. save result to database
5. return json data

## refine

1. 修正 `ModuleNotFoundError`
2. 使用 mock 技術測試 API 定義的 200 OK 和 404 Not Found 兩種情況
3. 修正 pytest 的 `ModuleNotFoundError`