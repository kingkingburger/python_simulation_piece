import pytest
import statistics
from src.distributions.normal import Normal
import pytest
import numpy as np
from src.distributions.normal import Normal


class TestNormal:
    """Normal 분포 테스트 클래스"""

    def test_init_valid_parameters(self):
        """유효한 매개변수로 초기화 테스트"""
        dist = Normal(mean=5.0, stddev=2.0)
        assert dist.mean == 5.0
        assert dist.stddev == 2.0

    def test_init_zero_stddev(self):
        """표준편차가 0인 경우 테스트"""
        dist = Normal(mean=0.0, stddev=0.0)
        assert dist.stddev == 0.0

    def test_init_negative_stddev_raises_error(self):
        """음수 표준편차 시 ValueError 발생 테스트"""
        with pytest.raises(ValueError, match="Standard deviation cannot be negative"):
            Normal(mean=0.0, stddev=-1.0)

    def test_generate_returns_float(self):
        """generate 메서드가 float 타입을 반환하는지 테스트"""
        dist = Normal(mean=0.0, stddev=1.0)
        result = dist.generate()
        assert isinstance(result, float)

    def test_generate_statistical_properties(self):
        """생성된 값들의 통계적 특성 테스트"""
        mean, stddev = 10.0, 2.0
        dist = Normal(mean=mean, stddev=stddev)

        # 충분한 샘플 생성
        samples = [dist.generate() for _ in range(10000)]

        # 표본 평균이 모집단 평균에 근사하는지 검증
        sample_mean = np.mean(samples)
        assert abs(sample_mean - mean) < 0.1

        # 표본 표준편차가 모집단 표준편차에 근사하는지 검증
        sample_stddev = np.std(samples, ddof=1)
        assert abs(sample_stddev - stddev) < 0.1

    def test_repr(self):
        """__repr__ 메서드 테스트"""
        dist = Normal(mean=1.5, stddev=0.5)
        expected = "Normal(mean=1.5, stddev=0.5)"
        assert repr(dist) == expected

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
