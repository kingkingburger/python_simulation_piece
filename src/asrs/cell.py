from typing import List, Optional
from .item import Item
from .position import Position


class Cell:
    """창고의 각 셀을 나타내는 클래스"""

    def __init__(self, position: Position):
        self.position = position
        self.items: List[Item] = []

    def add_item(self, item: Item):
        """셀에 아이템 추가"""
        self.items.append(item)

    def remove_item_fifo(self) -> Optional[Item]:
        """FIFO 방식으로 아이템 제거"""
        if self.items:
            return self.items.pop(0)
        return None

    def remove_item_lifo(self) -> Optional[Item]:
        """LIFO 방식으로 아이템 제거"""
        if self.items:
            return self.items.pop()
        return None

    def remove_item_priority(self) -> Optional[Item]:
        """우선순위 방식으로 아이템 제거 (높은 우선순위부터)"""
        if not self.items:
            return None

        # 우선순위가 가장 높은 아이템을 찾음
        highest_priority_item = max(self.items, key=lambda item: item.priority)
        self.items.remove(highest_priority_item)
        return highest_priority_item

    def is_empty(self) -> bool:
        """셀이 비어있는지 확인"""
        return len(self.items) == 0

    def get_items(self) -> List[Item]:
        """셀의 모든 아이템 반환"""
        return self.items.copy()
