from random import random
from typing import List, Optional, Dict

from .cell import Cell
from .config.storage_cost_policy import StorageCostPolicy, PerTimeUnitStrategy, \
    PerItemUnitStrategy
from .item import Item
from .output_policy import OutputPolicy, FIFOStrategy, LIFOStrategy, \
    PriorityStrategy
from .position import Position
from .stacker_crane import StackerCrane


class ASRS:
    """자동창고 시스템 메인 클래스"""

    def __init__(
        self,
        max_x: int,
        max_y: int,
        max_z: int,
        inbound_time: float = 1.0,
        outbound_time: float = 1.0,
        storage_cost_policy: StorageCostPolicy = StorageCostPolicy.PER_ITEM_UNIT,
        cost_item: float = 0.01,
        cost_time: float = 0.1,
        max_items_per_cell: int = 100
    ):
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z
        self.inbound_time = inbound_time
        self.outbound_time = outbound_time
        self.storage_cost_policy = storage_cost_policy
        self.storage_cost_strategies = {
            StorageCostPolicy.PER_TIME_UNIT: PerTimeUnitStrategy(),
            StorageCostPolicy.PER_ITEM_UNIT: PerItemUnitStrategy()
        }
        self.cost_item = cost_item
        self.cost_time = cost_time
        self.max_items_per_cell = max_items_per_cell
        self.cells: Dict[Position, Cell] = {}
        self.output_policy = OutputPolicy.FIFO
        self.strategies = {
            OutputPolicy.FIFO: FIFOStrategy(),
            OutputPolicy.LIFO: LIFOStrategy(),
            OutputPolicy.PRIORITY: PriorityStrategy()
        }
        self.stacker_crane = StackerCrane(self)

        # 모든 셀 초기화
        self._initialize_cells()

    def _initialize_cells(self):
        """모든 셀을 초기화"""
        for x in range(self.max_x):
            for y in range(self.max_y):
                for z in range(self.max_z):
                    position = Position(x, y, z)
                    self.cells[position] = Cell(position)

    def _is_valid_position(self, position: Position) -> bool:
        """위치가 유효한지 확인"""
        return (0 <= position.x < self.max_x and
                0 <= position.y < self.max_y and
                0 <= position.z < self.max_z)

    def calculate_storage_cost(self, items_count: int, time: float, cost: float) -> float:
        """
        보관유지비용 계산

        Args:
            items_count: 아이템 개수
            time: 시간
            cost: 비용
        Returns:
            계산된 보관유지비용
        """
        storage_cost_policy = self.storage_cost_strategies[
            self.storage_cost_policy]
        return storage_cost_policy.calculate(time, cost, items_count)

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

    def set_output_policy(self, policy: OutputPolicy):
        """출고 정책 설정"""
        self.output_policy = policy

    def put_item(self, item: Item, position: Position) -> bool:
        """아이템을 특정 위치에 입고"""
        if not self._is_valid_position(position):
            return False

        cell = self.cells[position]
        current_items_count = len(cell.get_items())

        # 셀 용량 확인
        if self.is_cell_full(current_items_count):
            return False

        cell.add_item(item)
        return True

    def get_item(self, position: Position) -> Optional[Item]:
        """특정 위치에서 출고 정책에 따라 아이템 출고"""
        if not self._is_valid_position(position):
            return None

        cell = self.cells[position]
        strategy = self.strategies[self.output_policy]
        return strategy.get_item(cell)

    def get_items_at_position(self, position: Position) -> List[Item]:
        """특정 위치의 모든 아이템 조회"""
        if not self._is_valid_position(position):
            return []

        cell = self.cells[position]
        return cell.get_items()

    def find_item_positions(self, item_id: str) -> List[Position]:
        """특정 아이템 ID의 모든 위치 찾기"""
        positions = []
        for position, cell in self.cells.items():
            for item in cell.get_items():
                if item.id == item_id:
                    positions.append(position)
                    break  # 같은 셀에서 중복 위치 방지
        return positions

    def stacker_crane_put(self, item: Item, position: Position) -> bool:
        """스태커크레인을 통한 입고"""
        return self.stacker_crane.put_item(item, position)

    def stacker_crane_get(self, position: Position) -> Optional[Item]:
        """스태커크레인을 통한 출고"""
        return self.stacker_crane.get_item(position)

    def get_total_items(self) -> int:
        """전체 아이템 수 반환"""
        total = 0
        for cell in self.cells.values():
            total += len(cell.get_items())
        return total

    def get_empty_cells(self) -> List[Position]:
        """빈 셀들의 위치 반환"""
        empty_positions = []
        for position, cell in self.cells.items():
            if cell.is_empty():
                empty_positions.append(position)
        return empty_positions

    def get_available_cells(self) -> List[Position]:
        """아직 용량이 남은 셀들의 위치 반환"""
        available_positions = []
        for position, cell in self.cells.items():
            current_items_count = len(cell.get_items())
            if not self.is_cell_full(current_items_count):
                available_positions.append(position)
        return available_positions

    def calculate_total_storage_cost(self, cost: float) -> float:
        """전체 보관유지비용 계산"""
        total_cost = 0.0
        # 설정된 x초 마다 설정값
        time = self.cost_time
        for cell in self.cells.values():
            items_count = len(cell.get_items())
            if items_count > 0:
                total_cost += self.calculate_storage_cost(items_count, time, cost)
        return total_cost

    def get_cell_capacity_info(self, position: Position) -> Optional[Dict[str, int]]:
        """특정 셀의 용량 정보 반환"""
        if not self._is_valid_position(position):
            return None

        cell = self.cells[position]
        current_items_count = len(cell.get_items())

        return {
            "current_items": current_items_count,
            "max_capacity": self.max_items_per_cell,
            "available_capacity": self.get_available_capacity(
                current_items_count)
        }
