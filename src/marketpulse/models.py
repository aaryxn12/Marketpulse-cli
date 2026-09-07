from dataclasses import dataclass, field

@dataclass
class Position:
    ticker: str
    shares: int
    price: float

    def market_value(self):
        return self.shares * self.price
    
    def daily_return(self, previous_price):
        return (self.price - previous_price) / previous_price
    
@dataclass
class Portfolio:
    positions: list[Position] = field(default_factory=list)

    def add_position(self, position):
        self.positions.append(position)

    def total_value(self):
        return sum(p.market_value() for p in self.positions)