import pytest
from src.asrs.config import ASRSConfig, StorageCostPolicy


class TestASRSConfig:
    """ASRS 설정 테스트"""

    def test_default_config(self):
        """기본 설정 테스트"""
        config = ASRSConfig()

        assert config.inbound_time == 1.0
        assert config.outbound_time == 1.0
        assert config.storage_cost_policy == StorageCostPolicy.PER_TIME_UNIT
        assert config.storage_cost_per_unit == 0.1
        assert config.max_items_per_cell == 100

    def test_custom_config(self):
        """사용자 정의 설정 테스트"""
        config = ASRSConfig(
            inbound_time=2.5,
            outbound_time=1.5,
            storage_cost_policy=StorageCostPolicy.PER_ITEM_UNIT,
            storage_cost_per_unit=0.05,
            max_items_per_cell=50
        )

        assert config.inbound_time == 2.5
        assert config.outbound_time == 1.5
        assert config.storage_cost_policy == StorageCostPolicy.PER_ITEM_UNIT
        assert config.storage_cost_per_unit == 0.05
        assert config.max_items_per_cell == 50

    def test_calculate_storage_cost_per_time_unit(self):
        """시간 단위당 보관비용 계산 테스트"""
        config = ASRSConfig(
            storage_cost_policy=StorageCostPolicy.PER_TIME_UNIT,
            storage_cost_per_unit=0.2
        )

        cost = config.calculate_storage_cost(items_count=10, time_units=5.0)
        assert cost == 1.0  # 0.2 * 5.0

    def test_calculate_storage_cost_per_item_unit(self):
        """아이템 단위당 보관비용 계산 테스트"""
        config = ASRSConfig(
            storage_cost_policy=StorageCostPolicy.PER_ITEM_UNIT,
            storage_cost_per_unit=0.3
        )

        cost = config.calculate_storage_cost(items_count=8, time_units=5.0)
        assert cost == 2.4  # 0.3 * 8

    def test_is_cell_full(self):
        """셀 용량 확인 테스트"""
        config = ASRSConfig(max_items_per_cell=5)

        assert not config.is_cell_full(0)
        assert not config.is_cell_full(3)
        assert not config.is_cell_full(4)
        assert config.is_cell_full(5)
        assert config.is_cell_full(10)

    def test_get_available_capacity(self):
        """남은 용량 계산 테스트"""
        config = ASRSConfig(max_items_per_cell=10)

        assert config.get_available_capacity(0) == 10
        assert config.get_available_capacity(3) == 7
        assert config.get_available_capacity(10) == 0
        assert config.get_available_capacity(15) == 0  # 음수 방지
