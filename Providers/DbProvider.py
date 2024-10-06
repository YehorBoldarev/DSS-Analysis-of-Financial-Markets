import sqlite3
from Core.Models.StockModel import StockModel


class DataProvider:
    def __init__(self):
        self.db_path = "DB/stock.db"
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def reset_stocks_to_inactive(self):
        # Construct the SQL query to update all values in the column
        query = f"UPDATE Stocks SET IsActive = 0"

        try:
            self.cursor.execute(query)
            self.conn.commit()

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

        self.close()

    def upsert_stock(self, stock: StockModel):
        try:
            # Check if the ticker already exists in the table
            self.cursor.execute("SELECT Id FROM Stocks WHERE Ticker = ?", (stock.ticker,))
            row = self.cursor.fetchone()

            if row:
                # If the ticker exists, update the record
                self.cursor.execute("""
                        UPDATE Stocks
                        SET FullName = ?, Sector = ?, Industry = ?, UpdatedAt = ?, IndustryMarketWeight = ?, IsActive = ?
                        WHERE Ticker = ?
                    """, (stock.full_name, stock.sector, stock.industry, stock.updated_at,
                          stock.industry_market_weight, stock.is_active, stock.ticker))
            else:
                # If the ticker doesn't exist, insert a new record
                self.cursor.execute("""
                        INSERT INTO Stocks (Ticker, FullName, Sector, Industry, UpdatedAt, IndustryMarketWeight, IsActive)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (stock.ticker, stock.full_name, stock.sector, stock.industry, stock.updated_at,
                          stock.industry_market_weight, stock.is_active))

            self.conn.commit()

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def close(self):
        self.conn.close()
