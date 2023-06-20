from dataclasses import dataclass

import requests as r
from bs4 import BeautifulSoup
from tabulate import tabulate


def get_fx_to_usd(currency):
    fx_url = f"https://www.google.com/finance/quote/{currency}-USD"
    resp = r.get(fx_url)
    soup = BeautifulSoup(resp.content, "html.parser")

    fx_rate = soup.find("div", {"data-last-price": True})
    fx = float(fx_rate["data-last-price"])
    return fx


def get_stock_information(ticker, exchange):
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    resp = r.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")

    price_div = soup.find("div", attrs={"data-last-price": True})
    price = float(price_div["data-last-price"])
    currency = price_div["data-currency-code"]

    usd_price = price
    if currency != "USD":
        fx = get_fx_to_usd(currency)
        usd_price = round(price * fx, 2)

    return {
        "ticker": ticker,
        "exchange": exchange,
        "price": price,
        "currency": currency,
        "usd_price": usd_price,
    }


@dataclass
class Stock:
    ticker: str
    exchange: str
    price: float = 0
    currency: str = "USD"
    usd_price: float = 0

    def __post_init__(self):
        stock_info = get_stock_information(self.ticker, self.exchange)

        if stock_info["ticker"] == self.ticker:
            self.price = stock_info["price"]
            self.currency = stock_info["currency"]
            self.usd_price = stock_info["usd_price"]


@dataclass
class Position:
    stock: Stock
    quantity: int


@dataclass
class Portfolio:
    positions: list[Position]

    def get_total_value(self):
        total_value = 0

        for position in self.positions:
            total_value += position.quantity * position.stock.usd_price

        return total_value


def display_portfolio_summary(portfolio):
    if not isinstance(portfolio, Portfolio):
        raise TypeError("Please provide an instance of the Portfolio type")

    portfolio_value = portfolio.get_total_value()

    position_data = []

    for position in sorted(
        portfolio.positions, key=lambda x: x.quantity * x.stock.usd_price, reverse=True
    ):
        market_value = position.quantity * position.stock.usd_price
        allocation = market_value / portfolio_value * 100

        position_data.append(
            [
                position.stock.ticker,
                position.stock.exchange,
                position.quantity,
                position.stock.usd_price,
                market_value,
                allocation,
            ]
        )

    headers = [
        "Ticker",
        "Exchange",
        "Quantity",
        "Price",
        "Market Value",
        "% Allocation",
    ]
    table = tabulate(
        position_data,
        headers=headers,
        tablefmt="psql",
        floatfmt=".2f",
    )

    print(table)
    print(f"Total portfolio value: ${portfolio_value:,.2f}.")


if __name__ == "__main__":
    stocks = [
        Stock("SHOP", "TSE"),  # CAD
        Stock("MSFT", "NASDAQ"),  # USD
        Stock("GOOGL", "NASDAQ"),
        Stock("BNS", "TSE"),
    ]

    positions = [
        Position(stock, quantity)
        for stock, quantity in zip(stocks, [10, 2, 30, 100])
    ]

    portfolio = Portfolio(positions)

    display_portfolio_summary(portfolio)

    # Stock -> Position -> Portfolio
