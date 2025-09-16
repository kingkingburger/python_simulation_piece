import pytest
import statistics
from src.distributions.exponential import Exponential


def test_exponential_initialization():
    """Exponential 분포 초기화 테스트"""
    exp = Exponential(2.0)
    assert exp.mean == 2.0


def test_exponential_zero_mean_raises_error():
    """평균이 0일 때 에러 발생 테스트"""
    with pytest.raises(ValueError, match="Mean for Exponential distribution must be positive"):
        Exponential(0.0)


def test_exponential_negative_mean_raises_error():
    """음수 평균일 때 에러 발생 테스트"""
    with pytest.raises(ValueError, match="Mean for Exponential distribution must be positive"):
        Exponential(-1.0)


def test_exponential_generate_positive_values():
    """Exponential 분포가 항상 양수값을 생성하는지 테스트"""
    exp = Exponential(1.0)

    for _ in range(1000):
        value = exp.generate()
        assert value >= 0.0


def test_exponential_generate_statistical_properties():
    """Exponential 분포의 통계적 특성 테스트"""
    mean = 5.0
    exp = Exponential(mean)

    samples = [exp.generate() for _ in range(10000)]
    sample_mean = statistics.mean(samples)

    # 평균이 기대값에 근사하는지 확인 (허용 오차 10%)
    assert abs(sample_mean - mean) < mean * 0.1


def test_exponential_repr():
    """__repr__ 메서드 테스트"""
    exp = Exponential(3.5)
    assert repr(exp) == "Exponential(mean=3.5)"
