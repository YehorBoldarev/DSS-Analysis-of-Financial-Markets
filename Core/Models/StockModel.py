class StockModel:
    def __init__(self, ticker: str, full_name: str, sector: str, sector_name: str, industry: str,
                 industry_name: str, updated_at: str, industry_market_weight: float, is_active: bool):
        self.ticker = ticker
        self.full_name = full_name
        self.sector = sector
        self.sector_name = sector_name
        self.industry = industry
        self.industry_name = industry_name
        self.updated_at = updated_at
        self.industry_market_weight = industry_market_weight
        self.is_active = is_active

    def __str__(self):
        # Кастомна поведінка для методу print
        return (f"Stock [Ticker: {self.ticker}, Name: {self.full_name}, Sector: {self.sector}, "
                f"Industry: {self.industry}, Updated At: {self.updated_at}], "
                f"Industry market weight: {self.industry_market_weight}, Is Active: {self.is_active}")

    def __repr__(self):
        return (f"Stock(Ticker={self.ticker}, FullName={self.full_name}, Sector={self.sector}, "
                f"Industry={self.industry}, UpdatedAt={self.updated_at}), "
                f"IndustryMarketWeight={self.industry_market_weight}, IsActive={self.is_active}")
