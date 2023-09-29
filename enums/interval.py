from enum import Enum


class Interval(str, Enum):
    i_unknown = "unknown"
    i_1m = "1m"
    i_2m = "2m"
    i_5m = "5m"
    i_15m = "15m"
    i_30m = "30m"
    i_60m = "60m"
    i_90m = "90m"
    i_1h = "1h"
    i_1d = "1d"
    i_5d = "5d"
    i_1wk = "1wk"
    i_1mo = "1mo",
    i_3mo = "3mo"

    def __str__(self) -> str:
        return self.value
