from datetime import datetime
import pandas as pd
import os


class TimeSeriesProvider:
    def __init__(self):
        self.folder_path = "DB/Files/"

    def save_ts_data(self, ticker: str, df: pd.DataFrame):
        ts = pd.Series(df["Close"], df.index)
        ts.to_csv(self.folder_path + ticker + ".csv", date_format='%Y-%m-%d')

    def delete_all_ts(self):
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error during file deleting: {file_path}: {e}")

    def read_ts_data(self, ticker: str):
        data = pd.read_csv(f"{self.folder_path}{ticker}.csv", index_col="Date")
        data.index = pd.to_datetime(data.index, format='%Y-%m-%d')
        start_date = datetime.now().replace(year=datetime.now().year - 4)
        date_to_filter = pd.Timestamp(start_date)
        return data[data.index > date_to_filter]

    # def read_ts_data(self, ticker: str):
    #     data = pd.read_csv(f"{self.folder_path}{ticker}.csv", index_col="Date")
    #     data.index = pd.to_datetime(data.index, format='%Y-%m-%d')
    #     return data
