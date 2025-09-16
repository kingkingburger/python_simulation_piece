import numpy as np

from src.distributions.base import Distribution


class Exponential(Distribution):
    """지수 분포(Exponential Distribution)."""

    def __init__(self, mean: float):
        """
        Args:
            mean (float): 분포의 평균. 람다(lambda)의 역수입니다.

        Raises:
            ValueError: 평균이 0보다 작거나 같은 경우 발생합니다.
        """
        if mean <= 0:
            raise ValueError("Mean for Exponential distribution must be positive.")
        self.mean = mean

    def generate(self) -> float:
        # scale(평균)을 직접 인자로 받습니다.
        return np.random.exponential(scale=self.mean)

    def __repr__(self) -> str:
        return f"Exponential(mean={self.mean})"
