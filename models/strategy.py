from abc import abstractmethod, ABC

from enums import ComparisonOperation
from models import Condition


class Strategy(ABC):

    @abstractmethod
    def test(self, conditions):
        pass

    def _evaluate_condition(self, condition: Condition):
        if condition.comparison_operation == ComparisonOperation.EQUAL_TO:
            return condition.left == condition.right
        elif condition.comparison_operation == ComparisonOperation.GREATER_THAN:
            return condition.left > condition.right
        elif condition.comparison_operation == ComparisonOperation.LESS_THAN:
            return condition.left < condition.right
        elif condition.comparison_operation == ComparisonOperation.GREATER_THAN_EQUAL_TO:
            return condition.left >= condition.right
        elif condition.comparison_operation == ComparisonOperation.LESS_THAN_EQUAL_TO:
            return condition.left <= condition.right
        else:
            raise ValueError("Invalid comparison operation")
