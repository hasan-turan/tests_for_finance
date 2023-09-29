from typing import SupportsIndex


class Scale:
    def __init__(self, start: float, end: float, step: float):
        self.start = start
        self.end = end
        self.step = step
