import pytest
import statistics
from src.distributions.exponential import Exponential
import pytest
import numpy as np
from src.distributions.exponential import Exponential


class TestExponential:
    """Exponential 분포 테스트 클래스"""

    def test_init_valid_parameters(self):
        """유효한 매개변수로 초기화 테스트"""
        dist = Exponential(mean=2.0)
        assert dist.mean == 2.0

    def test_init_zero_mean_raises_error(self):
        """평균이 0인 경우 ValueError 발생 테스트"""
        with pytest.raises(ValueError, match="Mean for Exponential distribution must be positive"):
            Exponential(mean=0.0)

    def test_init_negative_mean_raises_error(self):
        """음수 평균 시 ValueError 발생 테스트"""
        with pytest.raises(ValueError, match="Mean for Exponential distribution must be positive"):
            Exponential(mean=-1.0)

    def test_generate_returns_float(self):
        """generate 메서드가 float 타입을 반환하는지 테스트"""
        dist = Exponential(mean=1.0)
        result = dist.generate()
        assert isinstance(result, float)

    def test_generate_positive_values(self):
        """생성된 값이 항상 양수인지 테스트"""
        dist = Exponential(mean=5.0)

        # 충분한 샘플 생성하여 모든 값이 양수인지 확인
        for _ in range(1000):
            value = dist.generate()
            assert value >= 0

    def test_generate_statistical_properties(self):
        """생성된 값들의 통계적 특성 테스트"""
        mean = 3.0
        dist = Exponential(mean=mean)

        # 충분한 샘플 생성
        samples = [dist.generate() for _ in range(10000)]

        # 표본 평균이 모집단 평균에 근사하는지 검증
        sample_mean = np.mean(samples)
        assert abs(sample_mean - mean) < 0.2

        # 지수분포의 분산은 평균의 제곱과 같음
        expected_variance = mean ** 2
        sample_variance = np.var(samples, ddof=1)
        assert abs(sample_variance - expected_variance) < 1.0

    def test_repr(self):
        """__repr__ 메서드 테스트"""
        dist = Exponential(mean=4.5)
        expected = "Exponential(mean=4.5)"
        assert repr(dist) == expected

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


@pytest.mark.parametrize("mean", [1.0, 2.0, 5.0, 10.0])
def test_exponential_generate_statistical_properties(mean: float):
    """Exponential 분포의 통계적 특성 테스트"""
    exp = Exponential(mean)

    samples = [exp.generate() for _ in range(10000)]
    sample_mean = statistics.mean(samples)

    # 평균이 기대값에 근사하는지 확인 (허용 오차 10%)
    assert abs(sample_mean - mean) < mean * 0.1


def test_exponential_repr():
    """__repr__ 메서드 테스트"""
    exp = Exponential(3.5)
    assert repr(exp) == "Exponential(mean=3.5)"
