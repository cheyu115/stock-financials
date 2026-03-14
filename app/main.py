import csv

from pathlib import Path

from app.stock import StockStatistics, create_stock_record
from app.utils import get_string
from app.database import init_db, save_to_db
from app.yfinance_fetcher import fetch_stock_data

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_NAME = BASE_DIR / "data" / "history.csv"


def save_to_csv(record: StockStatistics, filepath: Path = CSV_NAME) -> None:
    """
    Saves a record to a csv file.
    Creates the file if it does not exist.
    """
    file_exists = filepath.is_file()
    headers = ["Date", "Symbol", "Price", "EPS", "Growth Rate", "PE ratio", "PEG ratio"]
    data = [
        record.date,
        record.ticker,
        record.price,
        record.eps,
        record.eps_growth,
        record.pe_ratio,
        record.peg_ratio,
    ]

    with open(filepath, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(headers)

        writer.writerow(data)


def main():
    init_db()

    ticker = get_string("ticker: ")

    print(f"fetch {ticker} data from yahoo finance.")
    stock_data = fetch_stock_data(ticker)

    if not stock_data:
        print(f"fetch {ticker} data failed.")
        return

    record = create_stock_record(ticker, stock_data)

    save_to_csv(record)
    print(f"saves {record} to file.")
    save_to_db(record)
    print(f"saves {record} to sqlite database (history.db).")


if __name__ == "__main__":
    print("test data: aapl")
    main()
