from .models import Position, Portfolio

def daily_returns_for_ticker(positions: list[Position]) -> list[float]:
    returns = []
    for i in range(1, len(positions)):
        returns.append(positions[i].daily_return(positions[i-1].price))
    return returns

def mean_return_for_ticker(positions: list[Position]) -> float:
    daily_returns = daily_returns_for_ticker(positions)
    mean_return = sum(daily_returns)/len(daily_returns)
    return mean_return

def format_report(daily_positions: dict[str, list[Position]]) -> str:
    report = []
    portfolio = Portfolio()
    for ticker, positions in daily_positions.items():
        mean_return = mean_return_for_ticker(positions)
        report.append(f"{ticker} : {mean_return:+.4%}")

        portfolio.add_position(positions[-1]) 

    tot_value = portfolio.total_value()
    report.append(f"Total Portfolio Value : {tot_value:.2f}")  

    return "\n".join(report)

        