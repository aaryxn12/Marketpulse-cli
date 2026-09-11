# marketpulse-cli

A command-line portfolio analytics tool and companion FastAPI service, built from
scratch while learning Python as part of my transition from Angular/TypeScript
engineering toward AI/Forward Deployed Engineering work.

## Why this project

I work in fintech (Prime Brokerage, hedge fund clients), so a portfolio analytics
tool is genuine domain overlap rather than a generic "todo app." It started as a
CLI tool and grew into a FastAPI service exposing the same core logic over HTTP —
the natural next step for turning a script into something deployable.

## What it does

Given a CSV of daily ticker prices (`Date, Ticker, Shares, Close`), it computes:

- Day-over-day and mean returns per ticker
- Total portfolio value based on the latest holdings
- The same data available two ways: a formatted CLI report, or a JSON API

## Structure

```
marketpulse-cli/
  data/sample_prices.csv       # sample data: Date, Ticker, Shares, Close
  src/marketpulse/
    models.py                  # Position, Portfolio dataclasses
    stats.py                   # daily/mean returns, formatted report
    cli.py                     # CLI entry point: argparse, custom exceptions, @timed decorator
    api.py                     # FastAPI service: routing, exception handlers,
                                # dependency injection, timing middleware
```

## Running the CLI

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m src.marketpulse.cli                              # uses data/sample_prices.csv
python -m src.marketpulse.cli --path data/sample_prices.csv # explicit path
python -m src.marketpulse.cli --help
```

## Running the API

```bash
uvicorn src.marketpulse.api:app --reload
```

Then visit `http://127.0.0.1:8000/docs` for interactive API docs, or hit the
endpoints directly:

- `GET /report` — full portfolio report
- `GET /report/{ticker}` — mean return for a single ticker
- Both accept an optional `?path=` query parameter to point at a different CSV

Bad input (a missing file, malformed row data) returns a clean JSON error with
the correct HTTP status code (404 / 422) instead of a raw traceback.

## Notes

Built end-to-end by hand, one function at a time — the git history reflects the
actual build (and debugging) process rather than a single "add everything" commit.
