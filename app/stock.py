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


def _valid_positive(x: float) -> bool:
    """返回 True 當且僅當 x 是正數。"""
    return x > 0


def calculate_pe_ratio(price: float, eps: float) -> float:
    """Price‑to‑Earnings (PE) ratio."""
    if _valid_positive(price) and _valid_positive(eps):
        return round(price / eps, 2)
    return 0.0


def calculate_peg_ratio(pe_ratio: float, eps_growth: float) -> float:
    """PEG ratio = PE / growth rate."""
    if _valid_positive(pe_ratio) and _valid_positive(eps_growth):
        return round(pe_ratio / eps_growth, 2)
    return 0.0


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
