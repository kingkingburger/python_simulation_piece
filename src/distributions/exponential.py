import random
from .base import Distribution


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
        # random.expovariate는 1/mean인 lambda를 인자로 받습니다.
        self.lambd = 1.0 / self.mean

    def generate(self) -> float:
        return random.expovariate(self.lambd)

    def __repr__(self) -> str:
        return f"Exponential(mean={self.mean})"
