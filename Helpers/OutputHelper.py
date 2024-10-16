import pandas as pd
from Providers.DbProvider import DataProvider
from Helpers.FinanceDataHelper import get_industry_weight_of_sector


def aggregate_industry_forecast_results(forecasts: pd.DataFrame):
    for ticker in forecasts.columns:
        ticker_pct_change = forecasts[ticker].pct_change()
        ticker_pct_change *= 100
        market_weight = DataProvider().get_market_weight_of_ticker(ticker)
        forecasts[ticker] = ticker_pct_change * float(market_weight)

    forecasts.dropna(inplace=True)

    result = pd.Series()
    for index, row_data in forecasts.iterrows():
        result.loc[index] = row_data.sum()

    return result


def aggregate_sector_forecast_results(forecasts: pd.DataFrame):
    db_provider = DataProvider()

    for industry_name in forecasts.columns:
        industry_key = db_provider.get_industry_key_by_name(industry_name)
        industry_market_weight = get_industry_weight_of_sector(industry_key)
        forecasts[industry_name] *= float(industry_market_weight)

    result = pd.Series()
    for index, row_data in forecasts.iterrows():
        result.loc[index] = row_data.sum()

    db_provider.close()
    return result

