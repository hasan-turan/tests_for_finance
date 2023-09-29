from typing import List

from prettytable import PrettyTable

from models import Order, Parameter, Pair


class ProfitLoss:
    def __init__(self, pair: Pair, parameters: List[Parameter]):
        self.pair = pair

        self.parameters = parameters

    def to_string(self):
        profit_or_loss_string = ""
        for parameter in self.parameters:
            profit_or_loss_string += f" {parameter.to_string()}"

        profit_or_loss_string += "\n"
        profit_or_loss_string += self.pair.to_string()

        return profit_or_loss_string
