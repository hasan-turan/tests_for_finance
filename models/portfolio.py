from typing import List
import pandas as pd

from enums import OrderSide, Interval
from models.pair import Pair
from models.stock import Stock


class Portfolio:
    def __init__(self, balance: float):
        self.__initial_balance = balance;
        self.balance = balance
        self.pairs: List[Pair] = []
        # self.stocks: List[Stock] = []

    def print_pairs(self, pair_List: List[Pair]):
        for pair in pair_List:
            print(f"{pair.to_string()}")
            for order in pair.orders:
                print(f"----{order.to_string()}")

    def add_pair(self, pair: Pair):
        self.pairs.append(pair)

    def print_orders(self):
        for pair in self.pairs:
            for order in pair.orders:
                order.print_order()

    def get_holdings(self) -> List[Pair]:
        return [p for p in self.pairs if p.signal_order[-1] == OrderSide.BUY]

    def print_holdings(self):
        holdings = self.get_holdings()
        self.print_pairs(holdings)

    def calculate_profit_or_loss(self):
        profit_or_loss = [0.0]
        for pair in self.pairs:
            profit_or_loss.append(pair.profit_or_loss)

        return profit_or_loss
