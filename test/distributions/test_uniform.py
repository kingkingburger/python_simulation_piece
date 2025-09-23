import pytest
from src.distributions.uniform import Uniform


def test_uniform_initialization():
    """Uniform 분포 초기화 테스트"""
    uniform = Uniform(0.0, 10.0)
    assert uniform.min_val == 0.0
    assert uniform.max_val == 10.0


def test_uniform_min_greater_than_max_raises_error():
    """min_val이 max_val보다 클 때 에러 발생 테스트"""
    with pytest.raises(ValueError, match="min_val cannot be greater than max_val"):
        Uniform(10.0, 5.0)


def test_uniform_equal_min_max_allowed():
    """min_val과 max_val이 같을 때 허용되는지 테스트"""
    uniform = Uniform(5.0, 5.0)
    assert uniform.min_val == 5.0
    assert uniform.max_val == 5.0


def test_uniform_generate_range():
    """Uniform 분포 생성값이 범위 내에 있는지 테스트"""
    uniform = Uniform(-5.0, 15.0)

    for _ in range(1000):
        value = uniform.generate()
        assert -5.0 <= value <= 15.0

import pytest
import numpy as np
from src.distributions.uniform import Uniform


class TestUniform:
    """Uniform 분포 테스트 클래스"""

    def test_init_valid_parameters(self):
        """유효한 매개변수로 초기화 테스트"""
        dist = Uniform(min_val=1.0, max_val=5.0)
        assert dist.min_val == 1.0
        assert dist.max_val == 5.0

    def test_init_equal_min_max(self):
        """최솟값과 최댓값이 같은 경우 테스트"""
        dist = Uniform(min_val=3.0, max_val=3.0)
        assert dist.min_val == 3.0
        assert dist.max_val == 3.0

    def test_init_invalid_range_raises_error(self):
        """최솟값이 최댓값보다 큰 경우 ValueError 발생 테스트"""
        with pytest.raises(ValueError, match="min_val cannot be greater than max_val"):
            Uniform(min_val=10.0, max_val=5.0)

    def test_generate_returns_float(self):
        """generate 메서드가 float 타입을 반환하는지 테스트"""
        dist = Uniform(min_val=0.0, max_val=1.0)
        result = dist.generate()
        assert isinstance(result, float)

    def test_generate_within_range(self):
        """생성된 값이 범위 내에 있는지 테스트"""
        min_val, max_val = 2.0, 8.0
        dist = Uniform(min_val=min_val, max_val=max_val)

        # 충분한 샘플 생성하여 범위 확인
        for _ in range(1000):
            value = dist.generate()
            assert min_val <= value <= max_val

    def test_generate_statistical_properties(self):
        """생성된 값들의 통계적 특성 테스트"""
        min_val, max_val = 0.0, 10.0
        dist = Uniform(min_val=min_val, max_val=max_val)

        # 충분한 샘플 생성
        samples = [dist.generate() for _ in range(10000)]

        # 균등분포의 평균: (min + max) / 2
        expected_mean = (min_val + max_val) / 2
        sample_mean = np.mean(samples)
        assert abs(sample_mean - expected_mean) < 0.1

        # 모든 값이 범위 내에 있는지 확인
        assert all(min_val <= sample <= max_val for sample in samples)

    def test_repr(self):
        """__repr__ 메서드 테스트"""
        dist = Uniform(min_val=1.0, max_val=5.0)
        expected = "Uniform(min_val=1.0, max_val=5.0)"
        assert repr(dist) == expected
def test_uniform_generate_distribution():
    """Uniform 분포의 균등성 테스트"""
    uniform = Uniform(0.0, 100.0)
    samples = [uniform.generate() for _ in range(10000)]

    # 각 구간에 대략 동일한 수의 샘플이 있는지 확인
    ranges = [(i*10, (i+1)*10) for i in range(10)]
    counts = []

    for min_r, max_r in ranges:
        count = sum(1 for s in samples if min_r <= s < max_r)
        counts.append(count)

    # 각 구간의 카운트가 대략 1000개 (±200) 정도여야 함
    for count in counts:
        assert 800 <= count <= 1200


def test_uniform_repr():
    """__repr__ 메서드 테스트"""
    uniform = Uniform(1.0, 9.0)
    assert repr(uniform) == "Uniform(min_val=1.0, max_val=9.0)"
