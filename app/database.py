import sqlite3
from pathlib import Path
from stock import StockStatistics

BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = BASE_DIR / 'data' / 'history.db'

def init_db() -> None:
    """
    初始化資料庫。如果資料庫不存在，建立 "history.db" 並初始化資料表。
    """
    # 建立連線 (若檔案不存在會自動建立)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 建立存放股票歷史紀錄的資料表 (若不存在)
    # 加入 UNIQUE(date, symbol) 確保同一天同一檔股票只有一筆紀錄
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            symbol TEXT,
            price REAL,
            eps REAL,
            growth_rate REAL,
            pe_ratio REAL,
            peg_ratio REAL,
            UNIQUE(date, symbol)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_to_db(record: StockStatistics) -> None:
    """
    將一筆 StockStatistics 紀錄存入 SQLite 資料庫中。
    如果「日期+股票名稱」重複，則更新為最新的一筆。
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 使用 ON CONFLICT(date, symbol) DO UPDATE 來處理重複紀錄
    cursor.execute('''
        INSERT INTO stock_history (date, symbol, price, eps, growth_rate, pe_ratio, peg_ratio)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(date, symbol) DO UPDATE SET
            price = excluded.price,
            eps = excluded.eps,
            growth_rate = excluded.growth_rate,
            pe_ratio = excluded.pe_ratio,
            peg_ratio = excluded.peg_ratio
    ''', (
        record.date, 
        record.ticker, 
        record.price, 
        record.eps, 
        record.eps_growth, 
        record.pe_ratio, 
        record.peg_ratio
    ))
    
    conn.commit()
    conn.close()