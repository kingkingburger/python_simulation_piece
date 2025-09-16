import pytest
from src.asrs.position import Position


class TestPosition:
    def test_position_creation(self):
        pos = Position(1, 2, 3)
        assert pos.x == 1
        assert pos.y == 2
        assert pos.z == 3

    def test_position_equality(self):
        pos1 = Position(1, 2, 3)
        pos2 = Position(1, 2, 3)
        pos3 = Position(1, 2, 4)
        assert pos1 == pos2
        assert pos1 != pos3

    def test_position_inequality_with_different_types(self):
        pos = Position(1, 2, 3)
        assert pos != "Position(1, 2, 3)"
        assert pos != (1, 2, 3)
        assert pos != None

    def test_position_hash(self):
        pos1 = Position(1, 2, 3)
        pos2 = Position(1, 2, 3)
        pos3 = Position(2, 2, 3)

        # 같은 좌표는 같은 해시값
        assert hash(pos1) == hash(pos2)
        # 다른 좌표는 다른 해시값
        assert hash(pos1) != hash(pos3)

    def test_position_as_dict_key(self):
        """Position을 딕셔너리 키로 사용할 수 있는지 테스트"""
        pos1 = Position(1, 2, 3)
        pos2 = Position(1, 2, 3)
        pos3 = Position(2, 2, 3)

        position_dict = {pos1: "value1", pos3: "value3"}

        # 같은 좌표로 접근 가능
        assert position_dict[pos2] == "value1"
        assert len(position_dict) == 2

    def test_position_repr(self):
        pos = Position(1, 2, 3)
        assert repr(pos) == "Position(1, 2, 3)"

    def test_position_negative_coordinates(self):
        pos = Position(-1, -2, -3)
        assert pos.x == -1
        assert pos.y == -2
        assert pos.z == -3

    def test_position_zero_coordinates(self):
        pos = Position(0, 0, 0)
        assert pos.x == 0
        assert pos.y == 0
        assert pos.z == 0
