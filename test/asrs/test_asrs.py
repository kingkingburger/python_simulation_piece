import pytest
from src.asrs import ASRS, Item, Position, OutputPolicy


class TestASRS:
    def setup_method(self):
        self.asrs = ASRS(max_x=3, max_y=3, max_z=3)
        self.item1 = Item("ITEM001", "First Item", priority=1)
        self.item2 = Item("ITEM002", "Second Item", priority=2)
        self.item3 = Item("ITEM003", "Third Item", priority=3)

    def test_asrs_initialization(self):
        assert self.asrs.max_x == 3
        assert self.asrs.max_y == 3
        assert self.asrs.max_z == 3
        assert len(self.asrs.cells) == 27  # 3*3*3

    def test_put_item(self):
        position = Position(0, 0, 0)
        success = self.asrs.put_item(self.item1, position)
        assert success is True
        assert len(self.asrs.get_items_at_position(position)) == 1

    def test_put_multiple_items_same_cell(self):
        position = Position(0, 0, 0)
        self.asrs.put_item(self.item1, position)
        self.asrs.put_item(self.item2, position)
        items = self.asrs.get_items_at_position(position)
        assert len(items) == 2

    def test_get_item_fifo(self):
        position = Position(0, 0, 0)
        self.asrs.set_output_policy(OutputPolicy.FIFO)
        self.asrs.put_item(self.item1, position)
        self.asrs.put_item(self.item2, position)

        retrieved_item = self.asrs.get_item(position)
        assert retrieved_item.id == "ITEM001"  # 먼저 들어간 것이 먼저 나옴

    def test_get_item_lifo(self):
        position = Position(0, 0, 0)
        self.asrs.set_output_policy(OutputPolicy.LIFO)
        self.asrs.put_item(self.item1, position)
        self.asrs.put_item(self.item2, position)

        retrieved_item = self.asrs.get_item(position)
        assert retrieved_item.id == "ITEM002"  # 나중에 들어간 것이 먼저 나옴

    def test_get_item_priority(self):
        position = Position(0, 0, 0)
        self.asrs.set_output_policy(OutputPolicy.PRIORITY)
        self.asrs.put_item(self.item1, position)  # priority=1
        self.asrs.put_item(self.item3, position)  # priority=3
        self.asrs.put_item(self.item2, position)  # priority=2

        retrieved_item = self.asrs.get_item(position)
        assert retrieved_item.id == "ITEM003"  # 우선순위가 가장 높음 (3)

    def test_get_item_from_empty_cell(self):
        position = Position(0, 0, 0)
        retrieved_item = self.asrs.get_item(position)
        assert retrieved_item is None

    def test_invalid_position(self):
        invalid_position = Position(5, 5, 5)  # 범위 초과
        success = self.asrs.put_item(self.item1, invalid_position)
        assert success is False

    def test_stacker_crane_operations(self):
        position = Position(1, 1, 1)
        # 스태커크레인을 통한 입고
        success = self.asrs.stacker_crane_put(self.item1, position)
        assert success is True

        # 스태커크레인을 통한 출고
        retrieved_item = self.asrs.stacker_crane_get(position)
        assert retrieved_item is not None
        assert retrieved_item.id == "ITEM001"

    def test_get_all_items_by_id(self):
        pos1 = Position(0, 0, 0)
        pos2 = Position(1, 1, 1)
        self.asrs.put_item(self.item1, pos1)
        self.asrs.put_item(self.item1, pos2)  # 같은 아이템을 다른 위치에

        positions = self.asrs.find_item_positions("ITEM001")
        assert len(positions) == 2
        assert pos1 in positions
        assert pos2 in positions

    def test_output_policy_change(self):
        """출고 정책 변경 테스트"""
        position = Position(0, 0, 0)
        self.asrs.put_item(self.item1, position)
        self.asrs.put_item(self.item2, position)

        # FIFO로 설정하고 테스트
        self.asrs.set_output_policy(OutputPolicy.FIFO)
        assert self.asrs.output_policy == OutputPolicy.FIFO

        # LIFO로 변경하고 테스트
        self.asrs.set_output_policy(OutputPolicy.LIFO)
        assert self.asrs.output_policy == OutputPolicy.LIFO

    def test_get_total_items(self):
        """전체 아이템 수 조회 테스트"""
        pos1 = Position(0, 0, 0)
        pos2 = Position(1, 1, 1)

        assert self.asrs.get_total_item_count() == 0

        self.asrs.put_item(self.item1, pos1)
        assert self.asrs.get_total_item_count() == 1

        self.asrs.put_item(self.item2, pos1)  # 같은 셀에 추가
        self.asrs.put_item(self.item3, pos2)  # 다른 셀에 추가
        assert self.asrs.get_total_item_count() == 3

    def test_get_empty_cells(self):
        """빈 셀 조회 테스트"""
        empty_cells = self.asrs.get_empty_cells()
        assert len(empty_cells) == 27  # 처음에는 모든 셀이 비어있음

        position = Position(0, 0, 0)
        self.asrs.put_item(self.item1, position)

        empty_cells = self.asrs.get_empty_cells()
        assert len(empty_cells) == 26  # 하나의 셀에 아이템이 들어감
        assert position not in empty_cells

    def test_get_items_at_invalid_position(self):
        """유효하지 않은 위치에서 아이템 조회 테스트"""
        invalid_position = Position(10, 10, 10)
        items = self.asrs.get_items_at_position(invalid_position)
        assert items == []

    def test_integration_scenario(self):
        """통합 시나리오 테스트"""
        # 여러 위치에 아이템들을 넣고
        positions = [Position(0, 0, 0), Position(1, 1, 1), Position(2, 2, 2)]
        items = [self.item1, self.item2, self.item3]

        for pos, item in zip(positions, items):
            success = self.asrs.stacker_crane_put(item, pos)
            assert success is True

        # 각각 다른 정책으로 출고해보기
        self.asrs.set_output_policy(OutputPolicy.PRIORITY)

        # 우선순위 순서대로 나와야 함 (item3=3, item2=2, item1=1)
        for expected_item in [self.item3, self.item2, self.item1]:
            # 해당 아이템이 있는 위치 찾기
            item_positions = self.asrs.find_item_positions(expected_item.id)
            assert len(item_positions) > 0

            # 그 위치에서 아이템 출고
            retrieved_item = self.asrs.stacker_crane_get(item_positions[0])
            assert retrieved_item.id == expected_item.id