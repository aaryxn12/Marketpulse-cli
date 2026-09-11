from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .cli import load_positions, CSVDataInvalidError, DataFileNotFoundError
from .stats import format_report, mean_return_for_ticker
import time

app = FastAPI()

class TickerReport(BaseModel):
    ticker: str
    mean_return: float

def get_positions(path: str = "data/sample_prices.csv"):
    return load_positions(path)

@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = str(elapsed)
    return response

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
def get_report(positions: dict = Depends(get_positions)):
    result = format_report(positions)
    return {"report": result}

@app.get("/report/{ticker}", response_model=TickerReport)
def get_ticker_report(ticker: str, positions: dict = Depends(get_positions)):
    ticker_positions = positions.get(ticker)
    if ticker_positions is None:
        raise HTTPException(status_code=404, detail="Ticker Not Found")
    return {"ticker": ticker, "mean_return": round(mean_return_for_ticker(ticker_positions), 4)}

