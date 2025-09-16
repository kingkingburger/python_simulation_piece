from typing import Optional
from .item import Item
from .position import Position


class StackerCrane:
    """스태커크레인을 나타내는 클래스"""

    def __init__(self, asrs_system):
        self.asrs_system = asrs_system
        self.current_position = Position(0, 0, 0)

    def move_to(self, position: Position):
        """스태커크레인을 특정 위치로 이동"""
        self.current_position = position

    def put_item(self, item: Item, position: Position) -> bool:
        """스태커크레인을 통한 입고 작업"""
        self.move_to(position)
        return self.asrs_system.put_item(item, position)

    def get_item(self, position: Position) -> Optional[Item]:
        """스태커크레인을 통한 출고 작업"""
        self.move_to(position)
        return self.asrs_system.get_item(position)
