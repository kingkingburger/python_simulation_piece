import pytest
from unittest.mock import Mock
from src.asrs.stacker_crane import StackerCrane
from src.asrs.item import Item
from src.asrs.position import Position


class TestStackerCrane:
    def setup_method(self):
        # ASRS 시스템을 모킹
        self.mock_asrs = Mock()
        self.stacker_crane = StackerCrane(self.mock_asrs)
        self.item = Item("ITEM001", "Test Item")
        self.position = Position(2, 3, 4)

    def test_stacker_crane_initialization(self):
        assert self.stacker_crane.asrs_system == self.mock_asrs
        assert self.stacker_crane.current_position == Position(0, 0, 0)

    def test_move_to(self):
        target_position = Position(5, 6, 7)
        self.stacker_crane.move_to(target_position)
        assert self.stacker_crane.current_position == target_position

    def test_put_item(self):
        # ASRS의 put_item이 True를 반환하도록 설정
        self.mock_asrs.put_item.return_value = True

        result = self.stacker_crane.put_item(self.item, self.position)

        # 위치가 올바르게 이동되었는지 확인
        assert self.stacker_crane.current_position == self.position
        # ASRS의 put_item이 호출되었는지 확인
        self.mock_asrs.put_item.assert_called_once_with(self.item, self.position)
        assert result is True

    def test_put_item_failure(self):
        # ASRS의 put_item이 False를 반환하도록 설정
        self.mock_asrs.put_item.return_value = False

        result = self.stacker_crane.put_item(self.item, self.position)

        assert self.stacker_crane.current_position == self.position
        self.mock_asrs.put_item.assert_called_once_with(self.item, self.position)
        assert result is False

    def test_get_item(self):
        # ASRS의 get_item이 아이템을 반환하도록 설정
        self.mock_asrs.get_item.return_value = self.item

        result = self.stacker_crane.get_item(self.position)

        # 위치가 올바르게 이동되었는지 확인
        assert self.stacker_crane.current_position == self.position
        # ASRS의 get_item이 호출되었는지 확인
        self.mock_asrs.get_item.assert_called_once_with(self.position)
        assert result == self.item

    def test_get_item_none(self):
        # ASRS의 get_item이 None을 반환하도록 설정
        self.mock_asrs.get_item.return_value = None

        result = self.stacker_crane.get_item(self.position)

        assert self.stacker_crane.current_position == self.position
        self.mock_asrs.get_item.assert_called_once_with(self.position)
        assert result is None

    def test_multiple_operations(self):
        """여러 작업을 연속으로 수행할 때의 위치 변화 테스트"""
        pos1 = Position(1, 1, 1)
        pos2 = Position(2, 2, 2)
        item1 = Item("ITEM001", "Item 1")
        item2 = Item("ITEM002", "Item 2")

        self.mock_asrs.put_item.return_value = True
        self.mock_asrs.get_item.return_value = item2

        # 첫 번째 위치에 아이템 저장
        self.stacker_crane.put_item(item1, pos1)
        assert self.stacker_crane.current_position == pos1

        # 두 번째 위치에서 아이템 가져오기
        result = self.stacker_crane.get_item(pos2)
        assert self.stacker_crane.current_position == pos2
        assert result == item2

        # 호출 횟수 확인
        assert self.mock_asrs.put_item.call_count == 1
        assert self.mock_asrs.get_item.call_count == 1
