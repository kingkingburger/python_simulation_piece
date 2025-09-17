import pytest
from src.asrs.asrs import ASRS
from src.asrs.config import ASRSConfig, StorageCostPolicy
from src.asrs.item import Item
from src.asrs.position import Position


class TestASRSEnhanced:
    """향상된 ASRS 기능 테스트"""

    def test_asrs_with_default_config(self):
        """기본 설정으로 ASRS 생성 테스트"""
        asrs = ASRS(2, 2, 2)

        assert asrs.config.inbound_time == 1.0
        assert asrs.config.outbound_time == 1.0
        assert asrs.config.max_items_per_cell == 100

    def test_asrs_with_custom_config(self):
        """사용자 정의 설정으로 ASRS 생성 테스트"""
        config = ASRSConfig(
            inbound_time=3.0,
            outbound_time=2.0,
            max_items_per_cell=5
        )
        asrs = ASRS(2, 2, 2, config)

        assert asrs.config.inbound_time == 3.0
        assert asrs.config.outbound_time == 2.0
        assert asrs.config.max_items_per_cell == 5

    def test_put_item_with_capacity_limit(self):
        """셀 용량 제한으로 입고 테스트"""
        config = ASRSConfig(max_items_per_cell=2)
        asrs = ASRS(2, 2, 2, config)
        position = Position(0, 0, 0)

        # 첫 번째 아이템 입고 성공
        item1 = Item("item1", "Item 1")
        assert asrs.put_item(item1, position) == True

        # 두 번째 아이템 입고 성공
        item2 = Item("item2", "Item 2")
        assert asrs.put_item(item2, position) == True

        # 세 번째 아이템 입고 실패 (용량 초과)
        item3 = Item("item3", "Item 3")
        assert asrs.put_item(item3, position) == False

        # 셀에 2개 아이템만 있는지 확인
        items = asrs.get_items_at_position(position)
        assert len(items) == 2

    def test_get_available_cells(self):
        """사용 가능한 셀 조회 테스트"""
        config = ASRSConfig(max_items_per_cell=2)
        asrs = ASRS(2, 1, 1, config)  # 2개 셀만 생성

        # 처음에는 모든 셀이 사용 가능
        available_cells = asrs.get_available_cells()
        assert len(available_cells) == 2

        # 첫 번째 셀을 가득 채움
        pos1 = Position(0, 0, 0)
        asrs.put_item(Item("item1", "Item 1"), pos1)
        asrs.put_item(Item("item2", "Item 2"), pos1)

        # 이제 1개 셀만 사용 가능
        available_cells = asrs.get_available_cells()
        assert len(available_cells) == 1
        assert Position(1, 0, 0) in available_cells

    def test_calculate_total_storage_cost_per_time(self):
        """시간 단위 전체 보관비용 계산 테스트"""
        config = ASRSConfig(
            storage_cost_policy=StorageCostPolicy.PER_TIME_UNIT,
            storage_cost_per_unit=0.1
        )
        asrs = ASRS(2, 1, 1, config)

        # 각 셀에 아이템 추가
        asrs.put_item(Item("item1", "Item 1"), Position(0, 0, 0))
        asrs.put_item(Item("item2", "Item 2"), Position(1, 0, 0))

        # 10시간 동안 보관비용 계산
        total_cost = asrs.calculate_total_storage_cost(10.0)
        # 2개 셀 * 0.1 * 10시간 = 2.0
        assert total_cost == 2.0

    def test_calculate_total_storage_cost_per_item(self):
        """아이템 단위 전체 보관비용 계산 테스트"""
        config = ASRSConfig(
            storage_cost_policy=StorageCostPolicy.PER_ITEM_UNIT,
            storage_cost_per_unit=0.2
        )
        asrs = ASRS(2, 1, 1, config)

        # 첫 번째 셀에 2개 아이템, 두 번째 셀에 1개 아이템
        pos1 = Position(0, 0, 0)
        pos2 = Position(1, 0, 0)
        asrs.put_item(Item("item1", "Item 1"), pos1)
        asrs.put_item(Item("item2", "Item 2"), pos1)
        asrs.put_item(Item("item3", "Item 3"), pos2)

        # 아이템 단위 보관비용 계산 (시간은 무시됨)
        total_cost = asrs.calculate_total_storage_cost(5.0)
        # (2개 아이템 * 0.2) + (1개 아이템 * 0.2) = 0.6
        assert total_cost == 0.6

    def test_get_cell_capacity_info(self):
        """셀 용량 정보 조회 테스트"""
        config = ASRSConfig(max_items_per_cell=5)
        asrs = ASRS(2, 2, 2, config)
        position = Position(0, 0, 0)

        # 빈 셀 정보
        info = asrs.get_cell_capacity_info(position)
        assert info["current_items"] == 0
        assert info["max_capacity"] == 5
        assert info["available_capacity"] == 5

        # 아이템 2개 추가 후
        asrs.put_item(Item("item1", "Item 1"), position)
        asrs.put_item(Item("item2", "Item 2"), position)

        info = asrs.get_cell_capacity_info(position)
        assert info["current_items"] == 2
        assert info["max_capacity"] == 5
        assert info["available_capacity"] == 3

        # 잘못된 위치에 대해서는 None 반환
        invalid_position = Position(10, 10, 10)
        assert asrs.get_cell_capacity_info(invalid_position) is None
