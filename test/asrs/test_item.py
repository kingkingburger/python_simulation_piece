import pytest
from datetime import datetime
from src.asrs.item import Item


class TestItem:
    def test_item_creation(self):
        item = Item("ITEM001", "Test Item", priority=5)
        assert item.id == "ITEM001"
        assert item.name == "Test Item"
        assert item.priority == 5
        assert isinstance(item.created_at, datetime)

    def test_item_default_priority(self):
        item = Item("ITEM002", "Default Priority Item")
        assert item.priority == 0

    def test_item_created_at_type(self):
        item = Item("ITEM003", "Time Test Item")
        assert isinstance(item.created_at, datetime)

    def test_item_attributes_immutable_after_creation(self):
        item = Item("ITEM004", "Immutable Test")
        original_created_at = item.created_at

        # 속성 변경
        item.name = "Changed Name"
        item.priority = 10

        # created_at은 변경되지 않아야 함
        assert item.created_at == original_created_at
        assert item.name == "Changed Name"
        assert item.priority == 10
