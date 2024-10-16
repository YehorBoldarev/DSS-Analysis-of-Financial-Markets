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
                        SET FullName = ?, Sector = ?, SectorName = ?, Industry = ?, IndustryName = ?, UpdatedAt = ?, 
                        IndustryMarketWeight = ?, IsActive = ?
                        WHERE Ticker = ?
                    """, (stock.full_name, stock.sector, stock.sector_name, stock.industry, stock.industry_name,
                          stock.updated_at, stock.industry_market_weight, stock.is_active, stock.ticker))
            else:
                # If the ticker doesn't exist, insert a new record
                self.cursor.execute("""
                        INSERT INTO Stocks (Ticker, FullName, Sector, SectorName, Industry, IndustryName, UpdatedAt, 
                        IndustryMarketWeight, IsActive)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (stock.ticker, stock.full_name, stock.sector, stock.sector_name, stock.industry,
                          stock.industry_name, stock.updated_at, stock.industry_market_weight, stock.is_active))

            self.conn.commit()

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_all_companies(self):
        query = """
        SELECT DISTINCT "FullName"
        FROM "Stocks"
        """

        self.cursor.execute(query)

        names = self.cursor.fetchall()

        return [name[0] for name in names]

    def get_ticker_by_company_name(self, name: str):
        query = """
        SELECT DISTINCT "Ticker"
        From "Stocks"
        WHERE "FullName" = ?
        """

        self.cursor.execute(query, (name,))

        ticker = self.cursor.fetchone()

        self.close()

        return ticker[0]

    def get_tickers_by_sector(self, sector_key: str):
        query = """
        SELECT "Ticker"
        FROM "Stocks"
        WHERE "Sector" = ?
          AND "IsActive" = 1;
        """

        self.cursor.execute(query, (sector_key,))

        tickers = self.cursor.fetchall()

        self.close()

        return [ticker[0] for ticker in tickers]

    def get_tickers_by_industry(self, industry_key):
        query = """
        SELECT "Ticker"
        FROM "Stocks"
        WHERE "Industry" = ?
          AND "IsActive" = 1;
        """

        self.cursor.execute(query, (industry_key,))

        tickers = self.cursor.fetchall()

        self.close()

        return [ticker[0] for ticker in tickers]

    def get_market_weight_of_ticker(self, ticker: str):
        query = """
        SELECT "IndustryMarketWeight"
        FROM "Stocks"
        WHERE "Ticker" = ?
        """

        self.cursor.execute(query, (ticker,))

        weights = self.cursor.fetchone()

        self.close()

        return weights[0]

    def get_industry_keys_by_sector(self, sector_key: str):
        query = """
        SELECT DISTINCT "Industry"
        FROM "Stocks"
        WHERE "Sector" = ?
          AND "IsActive" = 1;
        """

        self.cursor.execute(query, (sector_key,))

        industries = self.cursor.fetchall()

        self.close()

        return [industry[0] for industry in industries]

    def get_industry_key_by_name(self, industry_name: str):
        query = """
        SELECT DISTINCT "Industry"
        From "Stocks"
        WHERE "IndustryName" = ?
            AND "IsActive" = 1
        """

        self.cursor.execute(query, (industry_name,))

        industries = self.cursor.fetchall()

        return [industry[0] for industry in industries][0]

    def get_industry_names_by_sector(self, sector_name: str):
        query = """
        SELECT DISTINCT "IndustryName"
        FROM "Stocks"
        WHERE "SectorName" = ?
          AND "IsActive" = 1;
        """

        self.cursor.execute(query, (sector_name,))

        industry_names = self.cursor.fetchall()

        return [industry_name[0] for industry_name in industry_names]

    def get_sector_names_list(self):
        query = """
        SELECT DISTINCT "SectorName"
        FROM "Stocks"
        WHERE "IsActive" = 1;
        """

        self.cursor.execute(query)

        sector_names = self.cursor.fetchall()

        return [sector_name[0] for sector_name in sector_names]

    def get_sector_key_by_name(self, name: str):
        query = """
        SELECT DISTINCT "Sector"
        FROM "Stocks"
        WHERE "SectorName" = ? 
            AND "IsActive" = 1;
        """

        self.cursor.execute(query, (name,))

        sectors = self.cursor.fetchall()

        return [sector[0] for sector in sectors][0]

    def close(self):
        self.conn.close()
