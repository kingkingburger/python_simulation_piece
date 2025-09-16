import abc


class Distribution(abc.ABC):
    """
    모든 확률 분포 클래스를 위한 추상 기본 클래스(ABC).
    """

    @abc.abstractmethod
    def generate(self) -> float:
        """분포로부터 단일 샘플을 추출합니다."""
        pass
