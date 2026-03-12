實作兩項功能

# init_db
1. 初始化資料庫，如果資料庫不存在，建立 "history.db"
# save_to_db 
1. 將一筆 StockStatistics 紀錄存入 SQLite 資料庫
2. 如果「日期+股票名稱」重複，我們只儲存最新的一筆。