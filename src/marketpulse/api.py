from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from .cli import load_positions, CSVDataInvalidError, DataFileNotFoundError
from .stats import format_report, mean_return_for_ticker

app = FastAPI()

@app.exception_handler(DataFileNotFoundError)
def handle_file_not_found(request: Request, exc: DataFileNotFoundError):
    return JSONResponse(
        status_code = 404,
        content = {"error" : exc.err_msg}
    )
@app.exception_handler(CSVDataInvalidError)
def handle_invalid_file(request: Request, exc: CSVDataInvalidError):
    return JSONResponse(
        status_code = 422,
        content = {"error" : exc.err_msg}
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to MarketPulse API"}

@app.get("/report")
def get_report(path: str="data/sample_prices.csv"):
    positions = load_positions(path)
    result = format_report(positions)
    return {"report": result}

@app.get("/report/{ticker}")
def get_ticker_report(ticker: str, path: str = "data/sample_prices.csv"):
    positions = load_positions(path)
    ticker_positions = positions.get(ticker)
    if ticker_positions is None:
        raise HTTPException(status_code=404, detail="Ticker Not Found")
    return {"ticker": ticker, "mean_return": round(mean_return_for_ticker(ticker_positions), 4)}

