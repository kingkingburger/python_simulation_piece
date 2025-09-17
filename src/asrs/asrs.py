from typing import List, Optional, Dict
from .item import Item
from .position import Position
from .cell import Cell
from .output_policy import OutputPolicy, FIFOStrategy, LIFOStrategy, PriorityStrategy
from .stacker_crane import StackerCrane
from .config import ASRSConfig


class ASRS:
    """자동창고 시스템 메인 클래스"""

    def __init__(self, max_x: int, max_y: int, max_z: int, config: Optional[ASRSConfig] = None):
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z
        self.config = config or ASRSConfig()
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
        if self.config.is_cell_full(current_items_count):
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
            if not self.config.is_cell_full(current_items_count):
                available_positions.append(position)
        return available_positions

    def calculate_total_storage_cost(self, time_units: float) -> float:
        """전체 보관유지비용 계산"""
        total_cost = 0.0
        for cell in self.cells.values():
            items_count = len(cell.get_items())
            if items_count > 0:
                total_cost += self.config.calculate_storage_cost(items_count, time_units)
        return total_cost

    def get_cell_capacity_info(self, position: Position) -> Optional[Dict[str, int]]:
        """특정 셀의 용량 정보 반환"""
        if not self._is_valid_position(position):
            return None

        cell = self.cells[position]
        current_items_count = len(cell.get_items())

        return {
            "current_items": current_items_count,
            "max_capacity": self.config.max_items_per_cell,
            "available_capacity": self.config.get_available_capacity(current_items_count)
        }