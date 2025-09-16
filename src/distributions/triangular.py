import random
from .base import Distribution


class Triangular(Distribution):
    """삼각 분포(Triangular Distribution)."""

    def __init__(self, min_val: float, mode: float, max_val: float):
        """
        Args:
            min_val (float): 가능한 최솟값.
            mode (float): 최빈값 (가장 확률이 높은 값).
            max_val (float): 가능한 최댓값.

        Raises:
            ValueError: min_val <= mode <= max_val 조건이 만족되지 않을 경우 발생합니다.
        """
        if not (min_val <= mode <= max_val):
            raise ValueError("Condition min_val <= mode <= max_val must be met.")
        self.min_val = min_val
        self.mode = mode
        self.max_val = max_val

    def generate(self) -> float:
        return random.triangular(self.min_val, self.max_val, self.mode)

    def __repr__(self) -> str:
        return f"Triangular(min_val={self.min_val}, mode={self.mode}, max_val={self.max_val})"
