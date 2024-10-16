import yfinance as yf


def get_ticker_info(ticker: str):
    return yf.Ticker(ticker)


def get_price_history(ticker: str):
    ticker_info = yf.Ticker(ticker)
    return ticker_info.history(period='max')


def get_sector_name(sector_key: str):
    return yf.Sector(sector_key).name


def get_asset_industry(ticker_info: yf.Ticker):
    return yf.Industry(ticker_info.info.get('industryKey'))


def get_top_industry_companies(industry_key: str):
    industry = yf.Industry(industry_key)
    return industry.top_companies


def get_industry_weight_of_sector(industry_key: str):
    industry = yf.Industry(industry_key)
    sector = yf.Sector(industry.sector_key)
    return sector.industries["market weight"][industry.key]


def get_industries_in_sector(sector_key: str):
    sector = yf.Sector(sector_key)
    return sector.industries
