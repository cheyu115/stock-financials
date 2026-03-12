import csv
import datetime

from pathlib import Path

from stock import StockStatistics, calculate_pe_ratio, calculate_peg_ratio
from utils import get_string

from database import init_db, save_to_db
from yfinance_fetcher import fetch_stock_data

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_NAME = BASE_DIR / 'data' / 'history.csv'

def save_to_csv(record: StockStatistics, filepath: Path = CSV_NAME) -> None:
    """
    Saves a record to a csv file.
    Creates the file if it does not exist.
    """
    file_exists = filepath.is_file()
    headers = ['Date', 'Symbol', 'Price', 'EPS', 'Growth Rate', 'PE ratio', 'PEG ratio']
    data    = [record.date, record.ticker, record.price, record.eps, record.eps_growth, record.pe_ratio, record.peg_ratio]

    with open(filepath, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(headers)

        writer.writerow(data)

def main():
    init_db()

    ticker  = get_string('ticker: ')
    
    print(f"fetch {ticker} data from yahoo finance.")
    stock_data = fetch_stock_data(ticker)

    if not stock_data:
        print(f"fetch {ticker} data failed.")
        return

    pe_ratio = calculate_pe_ratio(stock_data.price, stock_data.eps)
    peg_ratio = calculate_peg_ratio(pe_ratio, stock_data.eps_growth)
    today_str = str(datetime.date.today())

    print(stock_data)

    record = StockStatistics(
        ticker=ticker,
        price=stock_data.price,
        eps=stock_data.eps,
        eps_growth=stock_data.eps_growth,
        pe_ratio=pe_ratio,
        peg_ratio=peg_ratio,
        date=today_str
    )

    save_to_csv(record)
    print(f'saves {record} to file.')
    save_to_db(record)
    print(f'saves {record} to sqlite database (history.db).')

if __name__ == "__main__":
    print("test data: aapl")
    main()
