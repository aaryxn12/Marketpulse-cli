import argparse, csv, sys
from .models import Position
from collections import defaultdict
from .stats import format_report

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
    
def main():
    parser = argparse.ArgumentParser(description="Welcome to MARKETPULSE CLI tool")
    parser.add_argument("--path", default="data/sample_prices.csv")
    args = parser.parse_args()

    try:
        positions = load_positions(args.path)
    except CSVDataInvalidError as e:
        print(f"Error : {e.err_msg}")
        sys.exit(1)
    except DataFileNotFoundError as e:
        print(f"Error : {e.err_msg}")
        sys.exit(1)
    if positions is not None:    
        print("Path Fetched Successfully\nFile Format looks good")
        result = format_report(positions)
        print(f"Result : \n{result}")

if __name__ == "__main__":
    main()


            

