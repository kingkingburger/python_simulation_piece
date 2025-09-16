import random

from src.distributions.base import Distribution

class Uniform(Distribution):
    """균등 분포(Uniform Distribution)."""

    def __init__(self, min_val: float, max_val: float):
        """
        Args:
            min_val (float): 가능한 최솟값 (포함).
            max_val (float): 가능한 최댓값 (포함).

        Raises:
            ValueError: min_val이 max_val보다 큰 경우 발생합니다.
        """
        if min_val > max_val:
            raise ValueError("min_val cannot be greater than max_val.")
        self.min_val = min_val
        self.max_val = max_val

    def generate(self) -> float:
        return random.uniform(self.min_val, self.max_val)

    def __repr__(self) -> str:
        return f"Uniform(min_val={self.min_val}, max_val={self.max_val})"
