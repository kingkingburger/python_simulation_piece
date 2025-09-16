from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional
from .item import Item
from .cell import Cell


class OutputPolicy(Enum):
    """출고 정책을 나타내는 열거형"""
    FIFO = "FIFO"
    LIFO = "LIFO"
    PRIORITY = "PRIORITY"


class OutputStrategy(ABC):
    """출고 전략을 위한 추상 클래스"""

    @abstractmethod
    def get_item(self, cell: Cell) -> Optional[Item]:
        pass


class FIFOStrategy(OutputStrategy):
    """FIFO 출고 전략"""

    def get_item(self, cell: Cell) -> Optional[Item]:
        return cell.remove_item_fifo()


class LIFOStrategy(OutputStrategy):
    """LIFO 출고 전략"""

    def get_item(self, cell: Cell) -> Optional[Item]:
        return cell.remove_item_lifo()


class PriorityStrategy(OutputStrategy):
    """우선순위 출고 전략"""

    def get_item(self, cell: Cell) -> Optional[Item]:
        return cell.remove_item_priority()
