import yfinance as yf
import pandas as pd


class TimeSeriesProvider:
    def __init__(self):
        self.folder_path = "DB/Files/"

    def get_ts_data(self, ticker: str, start_date=None):
        data = pd.DataFrame(yf.download(ticker, start_date, progress=False))
        ts = pd.Series(data["Adj Close"], data.index)
        ts.to_csv(self.folder_path + ticker + ".csv")

    def get_multiple_ts_data(self, tickers: list[str], start_date=None):
        data = pd.DataFrame(yf.download(tickers, start_date, progress=False))
        for ticker in tickers:
            ts = pd.Series(data[("Adj Close", ticker)], data.index, name=ticker).dropna()
            ts.to_csv(self.folder_path + ticker + ".csv")
