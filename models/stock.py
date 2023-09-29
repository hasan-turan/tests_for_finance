from enums import OrderSide
from models import Order
from typing import List


class Stock:

    def __init__(self, title: str, balance: float = 0.0):
        self.title = title
        self.balance = balance
        self.initial_balance=balance
