from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..asrs import ASRS


class StorageCostPolicy(Enum):
    """보관유지비용 정책"""
    PER_TIME_UNIT = "per_time_unit"
    PER_ITEM_UNIT = "per_item_unit"


class StorageCostStrategy(ABC):
    """보관 유지 비용 전략을 위한 추상 클래스"""

    @abstractmethod
    def calculate(self, context: "ASRS", item_count: int) -> float:
        pass


class PerTimeUnitStrategy(StorageCostStrategy):
    def calculate(self, context: "ASRS", item_count: int) -> float:
        base_cost = context.cost
        return base_cost * item_count


class PerItemUnitStrategy(StorageCostStrategy):
    """단위당(Per Item) 기본 정책: 보관된 각 엔티티의 설정된 비용 총합"""

    def calculate(self, context: "ASRS", item_count: int) -> float:
        all_items = context.get_total_items()
        base_cost = sum(item.storage_cost for item in all_items)
        return base_cost
