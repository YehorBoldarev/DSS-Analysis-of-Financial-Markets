from Providers.DbProvider import DataProvider
from Providers.TimeSeriesProvider import TimeSeriesProvider
from Helpers.FinanceDataHelper import *
from Core.Const import SECTORS_KEYS
from datetime import datetime
from Core.Models.StockModel import StockModel
import concurrent.futures
import time


class DataHelper():
    def __init__(self):
        self.ts_provider = TimeSeriesProvider()

    def update_all_data(self):
        DataProvider().reset_stocks_to_inactive()
        self.ts_provider.delete_all_ts()

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(self.update_data_by_sector, SECTORS_KEYS)

    def update_data_by_sector(self, sector_key: str):
        data_provider = DataProvider()
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        industries = get_industries_in_sector(sector_key)
        time.sleep(0.35)
        for industry_key, industry_info in industries.iterrows():
            companies = get_top_industry_companies(industry_key)
            time.sleep(0.35)
            for company_ticker, company_info in companies.iterrows():
                if company_info["market weight"] >= 0.01:
                    price_history = get_price_history(company_ticker)
                    time.sleep(0.35)
                    stock = StockModel(company_ticker, company_info["name"], sector_key, industry_key,
                                       updated_at, company_info["market weight"], True)
                    self.ts_provider.save_ts_data(company_ticker, price_history)
                    data_provider.upsert_stock(stock)

        data_provider.close()
        