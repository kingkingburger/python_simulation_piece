import pytest
import statistics
from src.distributions.normal import Normal


def test_normal_initialization():
    """Normal 분포 초기화 테스트"""
    normal = Normal(0.0, 1.0)
    assert normal.mean == 0.0
    assert normal.stddev == 1.0


def test_normal_negative_stddev_raises_error():
    """음수 표준편차로 초기화 시 에러 발생 테스트"""
    with pytest.raises(ValueError, match="Standard deviation cannot be negative"):
        Normal(0.0, -1.0)


def test_normal_zero_stddev_allowed():
    """표준편차 0은 허용되는지 테스트"""
    normal = Normal(5.0, 0.0)
    assert normal.mean == 5.0
    assert normal.stddev == 0.0


def test_normal_generate_statistical_properties():
    """Normal 분포의 통계적 특성 테스트"""
    mean, stddev = 10.0, 2.0
    normal = Normal(mean, stddev)

    samples = [normal.generate() for _ in range(10000)]

    # 평균과 표준편차가 기대값에 근사하는지 확인 (허용 오차 5%)
    sample_mean = statistics.mean(samples)
    sample_stddev = statistics.stdev(samples)

    assert abs(sample_mean - mean) < mean * 0.05
    assert abs(sample_stddev - stddev) < stddev * 0.05


def test_normal_repr():
    """__repr__ 메서드 테스트"""
    normal = Normal(1.5, 0.5)
    assert repr(normal) == "Normal(mean=1.5, stddev=0.5)"
