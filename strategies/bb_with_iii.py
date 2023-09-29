from typing import List

from enums import LogicalOperation, ComparisonOperation
from models import Condition, Strategy


class BbWithIII(Strategy):
    def test(self, conditions: List[Condition]):
        if not conditions:
            return False

        result = self._evaluate_condition(conditions[0])

        for i in range(1, len(conditions)):
            condition = conditions[i]
            if condition.logical_operation == LogicalOperation.AND:
                result = result and self._evaluate_condition(condition)
            elif condition.logical_operation == LogicalOperation.OR:
                result = result or self._evaluate_condition(condition)
            else:
                raise ValueError("Invalid logical operation")

        return result



