import csv
from .models import Position
from collections import defaultdict

class CSVDataInvalidError(Exception):
    def __init__(self, err_msg, ticker):
        self.ticker = ticker
        self.err_msg = f"{err_msg} : Row {self.ticker} should have Numbers"
        super().__init__(err_msg, ticker)

class DataFileNotFoundError(Exception):
    def __init__(self, err_msg, path):
        self.path = path
        self.err_msg = f"{err_msg} : Data file not found at path - {self.path}"
        super().__init__(err_msg, path)


def load_positions(path: str) -> dict[str,list[Position]]:
    try:
        with open(path) as file:
            reader = csv.DictReader(file)
            grouped = defaultdict(list)
            try:
                for row in reader:
                    row["Shares"] = int(row["Shares"])
                    row["Close"] = float(row["Close"])

                    position = Position(row["Ticker"], row["Shares"], row["Close"])
                    grouped[row["Ticker"]].append(position)
                return grouped
            except ValueError as e:
                raise CSVDataInvalidError(e, row["Ticker"])
    except FileNotFoundError as e:
        raise DataFileNotFoundError(e, path)


            

