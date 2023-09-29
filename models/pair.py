import copy
from datetime import datetime
from typing import List

import numpy
from prettytable import PrettyTable

import config
from enums import OrderSide
from models.stock import Stock
from models.order import Order
import numpy as np

from models.time_limit import TimeLimit
from utils import date_time_utils


class Pair:
    def __init__(self, base: Stock, counter: Stock):
        self.base = base
        self.counter = counter
        self.__orders: List[Order] = []
        self.profit_or_loss = 0.0
        self.data_start_time: numpy.datetime64 = None
        self.data_end_time: numpy.datetime64 = None

    def get_pair_title(self):
        return self.counter.title + "/" + self.base.title

    def get_buy_count(self):
        return len([x for x in self.__orders if x.side == OrderSide.BUY])

    def get_sell_count(self):
        return len([x for x in self.__orders if x.side == OrderSide.SELL])

    def clear_orders(self):
        self.__orders: List[Order] = []

    def get_orders(self):
        return self.__orders

    def add_order(self, order: Order):
        _order = copy.deepcopy(order);
        _order.index = len(self.__orders) + 1

        _order.profit_loss_ratio = ((_order.size - self.get_orders()[-1].size) / self.get_orders()[-1].size) * 100 if len(self.get_orders()) > 0 else 0.0
        if order.side == OrderSide.BUY and self.base.balance > 0:
            self.__orders.append(_order)
            self.profit_or_loss = self.calculate_profit_loss()
            self.counter.balance = order.quantity
            self.base.balance = 0.0

        elif order.side == OrderSide.SELL and self.counter.balance > 0:
            self.__orders.append(_order)
            self.profit_or_loss = self.calculate_profit_loss()
            self.base.balance = order.quantity * order.price
            self.counter.balance = 0.0

    def reset(self):
        self.base.balance = self.base.initial_balance
        self.counter.balance = self.counter.initial_balance
        self.clear_orders()
        self.profit_or_loss = 0.0
        self.data_start_time = None
        self.data_end_time = None

    def add_orders(self, orders: List[Order]):
        for o in orders:
            self.add_order(o)

    def calculate_profit_loss(self):

        # total_buys = sum([o.price * o.quantity for o in self.__orders if o.side == OrderSide.BUY])
        #
        # total_sells = sum([o.price * o.quantity for o in self.__orders if o.side == OrderSide.SELL])
        #
        # return total_sells - total_buys

        if len(self.__orders) > 0:
            if self.__orders[-1].side == OrderSide.SELL:
                return self.__orders[-1].price * self.__orders[-1].quantity
            elif self.__orders[-1].side == OrderSide.BUY:
                return self.__orders[-1].last_size
            else:
                return 0.0
        else:
            return 0.0

    def print_profit_or_loss(self):
        print(self.get_profit_or_loss_string())

    def get_last_buy_in(self, limit: TimeLimit):
        return self.get_pair_title() if len(self.get_orders()) > 0 and self.get_orders()[-1].side == OrderSide.BUY and self.get_orders()[
            -1].operation_date_diff.total_seconds() < limit.get_seconds() else ''

    def get_last_sell_in(self, limit: TimeLimit):

        return self.get_pair_title() if len(self.get_orders()) > 0 and self.get_orders()[-1].side == OrderSide.SELL and self.get_orders()[
            -1].operation_date_diff.total_seconds() < limit.get_seconds() else ''

    def to_string(self):
        data_period = ''
        if self.data_start_time is not None and self.data_end_time is not None:
            data_period = f"{date_time_utils.np_datetime_to_string(self.data_start_time, config.DATE_FORMAT)}-" \
                          f"{date_time_utils.np_datetime_to_string(self.data_end_time, config.DATE_FORMAT) if self.data_start_time is not None and self.data_end_time is not None else ''}"
        hold_pl_ratio = ''
        if len(self.get_orders()) > 0:
            hold_pl_ratio = (((self.get_orders()[0].quantity * self.get_orders()[-1].last_price) - self.base.initial_balance) / self.base.initial_balance) * 100

        pair_string = f" Pair:{self.get_pair_title()} " \
                      f" Fiat->Initial-Current :{self.base.initial_balance}-{self.base.balance}" \
                      f" Share->Initial-Current:{self.counter.initial_balance}-{self.counter.balance} " \
                      f" P-L:{self.profit_or_loss}" \
                      f" P-L(%): {(self.profit_or_loss / self.base.initial_balance) * 100} " \
                      f" Hold (%): {hold_pl_ratio}" \
                      f" Date Period:{data_period} \n"

        orders_table = PrettyTable()
        orders_table.field_names = Order.get_field_names()

        for o in self.__orders:
            orders_table.add_row(o.to_table_row())

        pair_string += orders_table.get_string()

        pair_string += "\n"
        return pair_string

    def get_profit_or_loss_string(self):
        return (f"Pair:{self.counter.title}/{self.base.title}  "
                f"Last Order Side:{self.__orders[-1].side if len(self.__orders) > 0 else ''} "
                f"Quantity:{self.counter.balance} "
                f"Profit Loss:{self.profit_or_loss} % {(self.profit_or_loss / 10000) * 100}")
