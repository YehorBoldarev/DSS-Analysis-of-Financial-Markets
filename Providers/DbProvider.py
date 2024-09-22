import sqlite3
from typing import Optional
from datetime import datetime
from Core.Models.StockModel import StockModel


class DataProvider:
    def __init__(self):
        self.db_path = "DB/stock.db"
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def _row_to_stock(self, row: sqlite3.Row) -> StockModel:
        # Перетворення рядка в об'єкт Stock
        return StockModel(
            id=row['Id'],
            ticker=row['Ticker'],
            full_name=row['FullName'],
            sector=row['Sector'],
            sub_sector=row['SubSector'],
            updated_at=row['UpdatedAt']
        )

    def get_stock_by_ticker(self, ticker: str) -> Optional[StockModel]:
        # Метод для отримання запису про акцію за її тикером
        select_query = '''
        SELECT * FROM Stocks WHERE Ticker = ?
        '''
        self.cursor.execute(select_query, (ticker,))
        row = self.cursor.fetchone()
        if row:
            return self._row_to_stock(row)
        return None

    def update_stock(self, ticker: str):
        update_query = '''
        UPDATE Stocks
        SET UpdatedAt = ?
        WHERE Ticker = ?
        '''
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute(update_query, (updated_at, ticker))
        self.conn.commit()

    def update_stocks(self, tickers: list[str]):
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tickers_array = '"' + '", "'.join(tickers) + '"'

        update_query = f'''
        UPDATE Stocks
        SET UpdatedAt = '{updated_at}'
        WHERE Ticker In ({tickers_array})
        '''

        self.cursor.execute(update_query)
        self.conn.commit()

    def close(self):
        # Закриття підключення до бази даних
        self.conn.close()
