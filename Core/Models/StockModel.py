from datetime import datetime
from typing import Optional


class StockModel:
    def __init__(self, id: int, ticker: str, full_name: Optional[str], sector: Optional[str],
                 sub_sector: Optional[str], updated_at: Optional[str]):
        self.id = id
        self.ticker = ticker
        self.full_name = full_name
        self.sector = sector
        self.sub_sector = sub_sector
        self.updated_at = updated_at

    def __str__(self):
        # Кастомна поведінка для методу print
        return (f"Stock [ID: {self.id}, Ticker: {self.ticker}, Name: {self.full_name}, Sector: {self.sector}, "
                f"SubSector: {self.sub_sector}, Updated At: {self.updated_at}]")

    def __repr__(self):
        return (f"Stock(Id={self.id}, Ticker={self.ticker}, FullName={self.full_name}, Sector={self.sector}, "
                f"SubSector={self.sub_sector}, UpdatedAt={self.updated_at})")
