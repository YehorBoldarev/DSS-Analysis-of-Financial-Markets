from datetime import datetime
import pandas as pd
from Helpers.DataHelper import scale_data, revert_scale
from Helpers.ModelingHelper import ModelingHelper
from Helpers.ForecastingHelper import ForecastingHelper
from Providers.TimeSeriesProvider import TimeSeriesProvider
from Providers.DbProvider import DataProvider
import concurrent.futures
from Core.Const import SECTORS_KEYS
import tensorflow.keras.backend as K
from Helpers.OutputHelper import aggregate_industry_forecast_results


def transform_data(ticker: str):
    data = TimeSeriesProvider().read_ts_data(ticker)

    if data.shape[0] < 50:
        window = 2
    else:
        window = 5

    scaled_data, min_val, range_val = scale_data(data)
    return data, window, scaled_data, min_val, range_val


def provide_modeling(ticker: str):
    data, window_size, scaled_data, min_val, range_val = transform_data(ticker)

    ModelingHelper().fit_model_for_data(ticker, scaled_data, window_size)


def provide_forecast(ticker: str, n_steps: int):
    data, window_size, scaled_data, min_val, range_val = transform_data(ticker)

    forecasted_time_indexes = pd.bdate_range(data.index[-1], periods=n_steps + 1)[1:]
    last_window = scaled_data[-window_size:].values.reshape(window_size, 1)

    scaled_forecast = ForecastingHelper().make_forecast(ticker, last_window, n_steps)

    forecast = revert_scale(scaled_forecast, min_val, range_val)
    forecast = pd.Series(forecast, index=forecasted_time_indexes)

    return forecast


def fit_models_by_industry(industry_key: str):
    tickers = DataProvider().get_tickers_by_industry(industry_key)
    print(f"industry_key = {industry_key}, {datetime.now()}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(provide_modeling, tickers)


def fit_models_by_sectors():
    for sector_key in SECTORS_KEYS:
        print(f"sector_key = {sector_key}, {datetime.now()}")
        industries = DataProvider().get_industry_keys_by_sector(sector_key)
        for industry_key in industries:
            fit_models_by_industry(industry_key)
            K.clear_session()
        print(f"sector {sector_key} end = {datetime.now()}")


def forecast_for_sector(sector_name: str, n_days: int):
    db_provider = DataProvider()

    industry_names = db_provider.get_industry_names_by_sector(sector_name)

    results_df = pd.DataFrame()

    for industry_name in industry_names:
        industry_results = forecast_for_industry(industry_name, n_days)
        weighted_industry_results = aggregate_industry_forecast_results(industry_results)
        results_df[industry_name] = weighted_industry_results

    return results_df


def forecast_for_industry(industry_name: str, n_days: int):
    db_provider = DataProvider()

    industry_key = db_provider.get_industry_key_by_name(industry_name)
    tickers = db_provider.get_tickers_by_industry(industry_key)

    results_df = pd.DataFrame()

    for ticker in tickers:
        ticker_last_data = TimeSeriesProvider().read_ts_data(ticker)[-15:]
        ticker_forecasts = provide_forecast(ticker, n_days)

        combined_series = pd.concat([ticker_last_data.iloc[:, 0], ticker_forecasts])
        results_df[ticker] = combined_series

    K.clear_session()

    return results_df


def forecast_for_asset(company_name: str, n_days: int):
    ticker = DataProvider().get_ticker_by_company_name(company_name)

    ticker_last_data = TimeSeriesProvider().read_ts_data(ticker)[-15:]
    ticker_forecasts = provide_forecast(ticker, n_days)

    combined_series = pd.concat([ticker_last_data.iloc[:, 0], ticker_forecasts])

    K.clear_session()

    return pd.Series(data=combined_series, index=combined_series.index, name=ticker)
