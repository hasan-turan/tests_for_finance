from datetime import datetime

from pandas import DataFrame

from enums import OrderSide, Interval
import utils
import pandas as pd

from prettytable import PrettyTable


class Order:

    def __init__(self,
                 base: str,
                 counter: str,
                 side: OrderSide,
                 date: datetime,
                 price: float,
                 quantity: float,
                 last_price: float,
                 interval: Interval):
        self.index = 0
        self.base = base
        self.counter = counter;
        self.side = side
        self.price = price
        self.quantity = quantity
        self.date = utils.date_time_utils.to_datetime(date)
        self.size = price * quantity
        self.last_size = last_price * quantity
        self.last_price = last_price
        self.operation_date_diff = self.__calculate_date_diff()
        self.interval = interval
        self.profit_loss_ratio = 0.0

    @staticmethod
    def get_field_names():
        return ['Index', 'Pair', 'Side', 'Price', 'Quantity', 'Date', 'Size', 'P/L %', 'Last Price', 'Days Before']

    def to_string(self):
        return f"Index: {self.index} \t" \
               f"Pair: {self.counter} / {self.base} \t" \
               f"side: {self.side} \t" \
               f"price:{self.price} \t" \
               f"quantity:{self.quantity} \t" \
               f"date:{self.date}  \t" \
               f"size:{self.size} \t" \
               f"P/L %:{self.profit_loss_ratio} \t" \
               f"last price:{self.last_price} \t" \
               f"op date diff:{self.operation_date_diff}"

    def to_table(self):
        table = PrettyTable()
        table.field_names = self.get_field_names()
        table.add_row(self.to_table_row())
        return table.get_string()

    def to_table_row(self):
        return [self.index,
                self.counter + "/" + self.base,
                self.side, self.price, self.quantity, self.date, self.size, self.profit_loss_ratio, self.last_price, self.operation_date_diff]

    def get_data_as_array(self):
        data = [self.base, self.counter, self.side, self.price, self.quantity, self.date, self.size, self.last_price, self.operation_date_diff]
        return data

    def __calculate_date_diff(self):
        return datetime.today() - self.date

    def print_order(self):
        print(self.to_table())
