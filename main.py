import csv
import datetime
import os

from stock import StockStatistics, calculate_pe_ratio, calculate_peg_ratio
from utils import get_float, get_string

from database import init_db, save_to_db

def save_to_csv(record: StockStatistics, filename: str = 'history.csv') -> None:
    """
    Saves a record to a csv file.
    Creates the file if it does not exist.
    """
    file_exists = os.path.isfile(filename)
    headers = ['Date', 'Symbol', 'Price', 'EPS', 'Growth Rate', 'PE ratio', 'PEG ratio']
    data    = [record.date, record.ticker, record.price, record.eps, record.eps_growth, record.pe_ratio, record.peg_ratio]

    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(headers)

        writer.writerow(data)

def main():
    init_db()


    ticker  = get_string('ticker: ')
    price = get_float('price: ')
    eps = get_float('eps: ')
    eps_growth = get_float('growth rate (%): ')

    pe_ratio = calculate_pe_ratio(price, eps)
    peg_ratio = calculate_peg_ratio(pe_ratio, eps_growth)
    today_str = str(datetime.date.today())

    record = StockStatistics(
        ticker=ticker,
        price=price,
        eps=eps,
        eps_growth=eps_growth,
        pe_ratio=pe_ratio,
        peg_ratio=peg_ratio,
        date=today_str
    )

    save_to_csv(record)
    print(f'saves {record} to file.')
    save_to_db(record)
    print(f'saves {record} to sqlite database (history.db).')

if __name__ == "__main__":
    print("test data: aapl, 268.8, 7.89, 9.37")
    main()
