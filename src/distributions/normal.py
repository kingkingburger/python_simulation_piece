import numpy as np

from src.distributions.base import Distribution


class Normal(Distribution):
    """정규 분포(Normal Distribution)."""

    def __init__(self, mean: float, stddev: float):
        """
        Args:
            mean (float): 분포의 평균 (mu).
            stddev (float): 분포의 표준편차 (sigma).

        Raises:
            ValueError: 표준편차가 0보다 작은 경우 발생합니다.
        """
        if stddev < 0:
            raise ValueError("Standard deviation cannot be negative.")
        self.mean = mean
        self.stddev = stddev

    def generate(self) -> float:
        return np.random.normal(loc=self.mean, scale=self.stddev)

    def __repr__(self) -> str:
        return f"Normal(mean={self.mean}, stddev={self.stddev})"
