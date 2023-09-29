from enums import ComparisonOperation, LogicalOperation


class Condition:
    def __init__(self, left: float, comparison_operation: ComparisonOperation, right: float, logical_operation: LogicalOperation):
        self.left = left
        self.comparison_operation = comparison_operation
        self.right = right
        self.logical_operation = logical_operation
