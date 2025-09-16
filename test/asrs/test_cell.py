import pytest
from src.asrs.cell import Cell
from src.asrs.item import Item
from src.asrs.position import Position


class TestCell:
    def setup_method(self):
        self.position = Position(1, 1, 1)
        self.cell = Cell(self.position)
        self.item1 = Item("ITEM001", "First Item", priority=1)
        self.item2 = Item("ITEM002", "Second Item", priority=2)
        self.item3 = Item("ITEM003", "Third Item", priority=3)

    def test_cell_creation(self):
        assert self.cell.position == self.position
        assert self.cell.is_empty() is True
        assert len(self.cell.get_items()) == 0

    def test_add_item(self):
        self.cell.add_item(self.item1)
        assert self.cell.is_empty() is False
        assert len(self.cell.get_items()) == 1
        assert self.cell.get_items()[0] == self.item1

    def test_add_multiple_items(self):
        self.cell.add_item(self.item1)
        self.cell.add_item(self.item2)
        assert len(self.cell.get_items()) == 2

    def test_remove_item_fifo(self):
        self.cell.add_item(self.item1)
        self.cell.add_item(self.item2)

        removed_item = self.cell.remove_item_fifo()
        assert removed_item == self.item1  # 먼저 들어간 것이 먼저 나옴
        assert len(self.cell.get_items()) == 1

    def test_remove_item_lifo(self):
        self.cell.add_item(self.item1)
        self.cell.add_item(self.item2)

        removed_item = self.cell.remove_item_lifo()
        assert removed_item == self.item2  # 나중에 들어간 것이 먼저 나옴
        assert len(self.cell.get_items()) == 1

    def test_remove_item_priority(self):
        self.cell.add_item(self.item1)  # priority=1
        self.cell.add_item(self.item3)  # priority=3
        self.cell.add_item(self.item2)  # priority=2

        removed_item = self.cell.remove_item_priority()
        assert removed_item == self.item3  # 우선순위가 가장 높음
        assert len(self.cell.get_items()) == 2

    def test_remove_from_empty_cell(self):
        assert self.cell.remove_item_fifo() is None
        assert self.cell.remove_item_lifo() is None
        assert self.cell.remove_item_priority() is None

    def test_get_items_returns_copy(self):
        self.cell.add_item(self.item1)
        items = self.cell.get_items()
        items.clear()  # 반환된 리스트를 수정

        # 원본 셀의 아이템은 영향받지 않아야 함
        assert len(self.cell.get_items()) == 1

    def test_priority_with_same_values(self):
        item_same_priority = Item("ITEM004", "Same Priority", priority=2)
        self.cell.add_item(self.item2)  # priority=2
        self.cell.add_item(item_same_priority)  # priority=2

        removed_item = self.cell.remove_item_priority()
        # 같은 우선순위일 때는 max() 함수의 동작에 따라 첫 번째가 선택됨
        assert removed_item in [self.item2, item_same_priority]
