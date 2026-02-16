import datetime
from stock import StockStatistics, calculate_pe_ratio, calculate_peg_ratio

def main():
    ticker  = input("stock: ").upper()
    price = float(input("price: "))
    eps = float(input("eps: "))
    eps_growth = float(input("growth rate (%): "))
    pe_ratio = calculate_pe_ratio(price, eps)
    peg_ratio = calculate_peg_ratio(pe_ratio, eps_growth)
    today_str = str(datetime.date.today())

    record = StockStatistics(ticker=ticker, price=price, eps=eps, eps_growth=eps_growth, pe_ratio=pe_ratio, peg_ratio=peg_ratio, date=today_str)

    print(record)
if __name__ == "__main__":
    print("test data: aapl, 156, 7.9, 9.46")
    main()
