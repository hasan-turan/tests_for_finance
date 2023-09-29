from enum import Enum


class LineStyle(Enum):
    SOLID = "solid"  # Same as (0, ()) or '-'
    DOTTED="dotted" # Same as (0, (1, 1)) or ':'
    DASHED = "dashed"  # Same as '--'
    DASHDOT="dashdot" # Same as '-.'


