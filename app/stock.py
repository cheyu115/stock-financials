import datetime
from app.yfinance_fetcher import YfinanceData


class StockStatistics:
    """
    Records the statistical metrics of a stock.

    Attributes:
        ticker      (str):      stock ticker symbol
        price       (float):    current stock price
        eps         (float):    earnings per share
        eps_growth  (float):    estimated EPS growth rate for the next year
        pe_ratio    (float):    price-to-earnings ratio
        peg_ratio   (float):    PE-to-growth ratio
        date        (str):      date of the record, formatted as 'YYYY-MM-DD'
    """

    def __init__(
        self,
        ticker: str,
        price: float,
        eps: float,
        eps_growth: float,
        pe_ratio: float,
        peg_ratio: float,
        date: str,
    ) -> None:
        self.ticker = ticker
        self.price = price
        self.eps = eps
        self.eps_growth = eps_growth
        self.pe_ratio = pe_ratio
        self.peg_ratio = peg_ratio
        self.date = date

    def __str__(self) -> str:
        return f"[{self.date}: Price={self.price}, PE={self.pe_ratio}, PEG={self.peg_ratio}]"


def calculate_pe_ratio(price: float, eps: float) -> float:
    """
    Calculate the price to earnings (PE) ratio.
    Formula: price / EPS

    >>> calculate_pe_ratio(400, 0)
    0.0
    >>> calculate_pe_ratio(400, 20)
    20.0
    """
    if eps <= 0:
        return 0.0
    return round(price / eps, 1)


def calculate_peg_ratio(pe_ratio: float, eps_growth: float) -> float:
    """
    Calculate the PEG ratio.
    Formula: PE ratio / growth rate

    growth rate: yahoo finance analysis -> growth estimates -> next year column
    >>> calculate_peg_ratio(25, 0)
    0.0
    >>> calculate_peg_ratio(25, 15)
    1.67
    """
    if eps_growth <= 0:
        return 0.0
    return round(pe_ratio / eps_growth, 2)


def create_stock_record(ticker: str, stock_data: YfinanceData) -> StockStatistics:
    """
    將外部抓取的 YfinanceData 轉換成我們內部的 StockStatistics 紀錄。
    在這裡統一計算 PE, PEG 並壓上今天的日期。
    """
    pe_ratio = calculate_pe_ratio(stock_data.price, stock_data.eps)
    peg_ratio = calculate_peg_ratio(pe_ratio, stock_data.eps_growth)
    today_str = str(datetime.date.today())

    return StockStatistics(
        ticker=ticker.upper(),  # 統一轉成大寫
        price=stock_data.price,
        eps=stock_data.eps,
        eps_growth=stock_data.eps_growth,
        pe_ratio=pe_ratio,
        peg_ratio=peg_ratio,
        date=today_str,
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
