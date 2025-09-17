from abc import ABC, abstractmethod
from enum import Enum


class StorageCostPolicy(Enum):
    """보관유지비용 정책"""
    PER_TIME_UNIT = "per_time_unit"
    PER_ITEM_UNIT = "per_item_unit"


class StorageCostStrategy(ABC):
    """보관 유지 비용 전략을 위한 추상 클래스"""

    @abstractmethod
    def calculate(self, time: float, cost: float, item_count: int) -> float:
        pass


class PerTimeUnitStrategy(StorageCostStrategy):
    def calculate(self, time: float, cost: float, _item_count: int) -> float:
        return time * cost


class PerItemUnitStrategy(StorageCostStrategy):
    """단위당(Per Item) 기본 정책: 보관된 각 엔티티에 대해 시간 단위당 비용을 부과"""
    def calculate(self, time: float, cost: float, item_count: int) -> float:
        return time * cost * item_count
