from typing import List

from enums.line_styles import LineStyle
from models.signal import Signal


class IndicatorLine:
    def __init__(self, title: str, data: List[float], color: str, line_style: LineStyle = LineStyle.SOLID):
        self.title: str = title
        self.__data: List[float] = data
        self.color: str = color
        self.line_style: LineStyle = line_style

    def add_data_item(self, data_item: float):
        self.__data.append(data_item)

    def clear_data(self):
        self.__data.clear()

    def get_data(self):
        return self.__data
