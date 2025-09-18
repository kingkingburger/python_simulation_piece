from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..asrs import ASRS


class StorageCostPolicy(Enum):
    """보관유지비용 정책"""
    PER_TIME_UNIT = "per_time_unit"


class StorageCostStrategy(ABC):
    """보관 유지 비용 전략을 위한 추상 클래스"""

    @abstractmethod
    def calculate(self, context: "ASRS", item_count: int) -> float:
        pass


class PerTimeUnitStrategy(StorageCostStrategy):
    def calculate(self, context: "ASRS", item_count: int) -> float:
        base_cost = context.cost
        return base_cost * item_count
