import pytest
from src.asrs.output_policy import OutputPolicy, FIFOStrategy, LIFOStrategy, PriorityStrategy
from src.asrs.cell import Cell
from src.asrs.item import Item
from src.asrs.position import Position


class TestOutputPolicy:
    def test_output_policy_enum(self):
        assert OutputPolicy.FIFO.value == "FIFO"
        assert OutputPolicy.LIFO.value == "LIFO"
        assert OutputPolicy.PRIORITY.value == "PRIORITY"


class TestOutputStrategies:
    def setup_method(self):
        self.position = Position(0, 0, 0)
        self.cell = Cell(self.position)
        self.item1 = Item("ITEM001", "First Item", priority=1)
        self.item2 = Item("ITEM002", "Second Item", priority=2)
        self.item3 = Item("ITEM003", "Third Item", priority=3)

        self.fifo_strategy = FIFOStrategy()
        self.lifo_strategy = LIFOStrategy()
        self.priority_strategy = PriorityStrategy()

    def test_fifo_strategy(self):
        self.cell.add_item(self.item1)
        self.cell.add_item(self.item2)
        self.cell.add_item(self.item3)

        # FIFO: 첫 번째로 들어간 아이템이 먼저 나옴
        retrieved_item = self.fifo_strategy.get_item(self.cell)
        assert retrieved_item == self.item1

        retrieved_item = self.fifo_strategy.get_item(self.cell)
        assert retrieved_item == self.item2

    def test_lifo_strategy(self):
        self.cell.add_item(self.item1)
        self.cell.add_item(self.item2)
        self.cell.add_item(self.item3)

        # LIFO: 마지막으로 들어간 아이템이 먼저 나옴
        retrieved_item = self.lifo_strategy.get_item(self.cell)
        assert retrieved_item == self.item3

        retrieved_item = self.lifo_strategy.get_item(self.cell)
        assert retrieved_item == self.item2

    def test_priority_strategy(self):
        self.cell.add_item(self.item1)  # priority=1
        self.cell.add_item(self.item3)  # priority=3
        self.cell.add_item(self.item2)  # priority=2

        # Priority: 우선순위가 높은 아이템이 먼저 나옴
        retrieved_item = self.priority_strategy.get_item(self.cell)
        assert retrieved_item == self.item3  # priority=3

        retrieved_item = self.priority_strategy.get_item(self.cell)
        assert retrieved_item == self.item2  # priority=2

    def test_strategies_with_empty_cell(self):
        # 빈 셀에서는 모든 전략이 None을 반환
        assert self.fifo_strategy.get_item(self.cell) is None
        assert self.lifo_strategy.get_item(self.cell) is None
        assert self.priority_strategy.get_item(self.cell) is None

    def test_strategies_with_single_item(self):
        self.cell.add_item(self.item1)

        # 아이템이 하나일 때는 모든 전략이 같은 결과
        # 각각 별도의 셀에서 테스트
        cell1 = Cell(Position(0, 0, 0))
        cell2 = Cell(Position(0, 0, 1))
        cell3 = Cell(Position(0, 0, 2))

        cell1.add_item(Item("TEST1", "Test", priority=5))
        cell2.add_item(Item("TEST2", "Test", priority=5))
        cell3.add_item(Item("TEST3", "Test", priority=5))

        fifo_result = self.fifo_strategy.get_item(cell1)
        lifo_result = self.lifo_strategy.get_item(cell2)
        priority_result = self.priority_strategy.get_item(cell3)

        assert fifo_result.id == "TEST1"
        assert lifo_result.id == "TEST2"
        assert priority_result.id == "TEST3"
