# marketpulse-cli

A command-line portfolio analytics tool, built while learning Python as part of my
transition from Angular/TypeScript engineering toward AI/FDE work. This repo grows
in place across six weeks — each commit maps to a stage in that plan, so the history
itself shows the learning curve rather than hiding it.

## Why this project

I work in fintech (Prime Brokerage, hedge fund clients) and I'm prepping CFA Level 1,
so a portfolio analytics tool is genuine domain overlap rather than a generic
"todo app" — and it evolves directly into a FastAPI service (Phase 1 deliverable)
and later feeds into a RAG-based financial document Q&A agent (Phase 2).

## Roadmap for this repo

- **Week 1-2 — Python fundamentals.** Core syntax, functions, OOP, list comprehensions.
  Works today on a local CSV, no network calls yet, no error handling yet.
  (`src/marketpulse/models.py`, `stats.py`, `cli.py`)
- **Week 3-4 — Intermediate Python.** Swap the hardcoded CSV for real file I/O
  reading arbitrary paths, add proper error handling (bad tickers, missing dates,
  malformed rows), add a caching decorator, move config to a `.env` + `python-dotenv`,
  set up a virtual environment and pin dependencies properly.
- **Week 5-6 — FastAPI.** Wrap the same `stats.py` / `models.py` logic in a FastAPI
  service: `GET /portfolio/{id}/stats`, `POST /portfolio`, `GET /ticker/{symbol}/returns`.
  Pydantic models replace the hand-rolled dataclasses where it makes sense.

## Current status: Week 1 skeleton

Run it:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.marketpulse.cli data/sample_prices.csv
```

## Structure

```
marketpulse-cli/
  data/sample_prices.csv       # sample data, Date/Ticker/Close
  src/marketpulse/
    models.py                  # Position, Portfolio (OOP practice)
    stats.py                   # returns/volatility (list comprehensions, functions)
    cli.py                     # entry point
  tests/                       # added Week 3-4
```
