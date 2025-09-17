from enum import Enum
from typing import Optional


class StorageCostPolicy(Enum):
    """보관유지비용 정책"""
    PER_TIME_UNIT = "per_time_unit"
    PER_ITEM_UNIT = "per_item_unit"


class ASRSConfig:
    """ASRS 설정 클래스"""

    def __init__(
        self,
        inbound_time: float = 1.0,
        outbound_time: float = 1.0,
        storage_cost_policy: StorageCostPolicy = StorageCostPolicy.PER_TIME_UNIT,
        storage_cost_per_unit: float = 0.1,
        max_items_per_cell: int = 100
    ):
        """
        ASRS 설정 초기화

        Args:
            inbound_time: 입고 소요시간 (분)
            outbound_time: 출고 소요시간 (분)
            storage_cost_policy: 보관유지비용 정책 (시간 단위당/아이템 단위당)
            storage_cost_per_unit: 단위당 보관유지비용
            max_items_per_cell: 셀당 가능 개체 개수
        """
        self.inbound_time = inbound_time
        self.outbound_time = outbound_time
        self.storage_cost_policy = storage_cost_policy
        self.storage_cost_per_unit = storage_cost_per_unit
        self.max_items_per_cell = max_items_per_cell

    def calculate_storage_cost(self, items_count: int, time_units: float) -> float:
        """
        보관유지비용 계산

        Args:
            items_count: 아이템 개수
            time_units: 시간 단위

        Returns:
            계산된 보관유지비용
        """
        if self.storage_cost_policy == StorageCostPolicy.PER_TIME_UNIT:
            return self.storage_cost_per_unit * time_units
        else:  # PER_ITEM_UNIT
            return self.storage_cost_per_unit * items_count

    def is_cell_full(self, current_items_count: int) -> bool:
        """
        셀이 가득 찼는지 확인

        Args:
            current_items_count: 현재 셀의 아이템 개수

        Returns:
            셀이 가득 찼으면 True, 아니면 False
        """
        return current_items_count >= self.max_items_per_cell

    def get_available_capacity(self, current_items_count: int) -> int:
        """
        셀의 남은 용량 반환

        Args:
            current_items_count: 현재 셀의 아이템 개수

        Returns:
            남은 용량
        """
        return max(0, self.max_items_per_cell - current_items_count)
