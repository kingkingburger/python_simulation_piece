from typing import Union
from .base import Distribution


class Constant(Distribution):
    """항상 동일한 상수 값을 반환하는 분포."""

    def __init__(self, value: Union[int, float]):
        """
        Args:
            value (Union[int, float]): 반환될 상수 값.
        """
        self.value = value

    def generate(self) -> float:
        return float(self.value)

    def __repr__(self) -> str:
        return f"Constant(value={self.value})"
