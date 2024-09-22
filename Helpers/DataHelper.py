from Providers.DbProvider import DataProvider
from Providers.TimeSeriesProvider import TimeSeriesProvider

class DataHelper():
    def __init__(self):
        self.data_provider = DataProvider()
        self.ts_provider = TimeSeriesProvider()

    def update_time_series(self, tickers: list[str], start_date=None):
        self.ts_provider.get_multiple_ts_data(tickers, start_date)
        self.data_provider.update_stocks(tickers)
