import pytest
from src.distributions.triangular import Triangular


def test_triangular_initialization():
    """Triangular 분포 초기화 테스트"""
    tri = Triangular(0.0, 5.0, 10.0)
    assert tri.min_val == 0.0
    assert tri.mode == 5.0
    assert tri.max_val == 10.0


def test_triangular_invalid_order_raises_error():
    """min_val <= mode <= max_val 조건 위반 시 에러 테스트"""
    # mode가 min_val보다 작은 경우
    with pytest.raises(ValueError, match="Condition min_val <= mode <= max_val must be met"):
        Triangular(5.0, 2.0, 10.0)

    # mode가 max_val보다 큰 경우
    with pytest.raises(ValueError, match="Condition min_val <= mode <= max_val must be met"):
        Triangular(0.0, 15.0, 10.0)

    # min_val이 max_val보다 큰 경우
    with pytest.raises(ValueError, match="Condition min_val <= mode <= max_val must be met"):
        Triangular(10.0, 5.0, 5.0)


def test_triangular_boundary_values_allowed():
    """경계값들이 같을 때 허용되는지 테스트"""
    # min_val == mode
    tri1 = Triangular(0.0, 0.0, 10.0)
    assert tri1.min_val == tri1.mode == 0.0
import pytest
import numpy as np
from src.distributions.triangular import Triangular


class TestTriangular:
    """Triangular 분포 테스트 클래스"""

    def test_init_valid_parameters(self):
        """유효한 매개변수로 초기화 테스트"""
        dist = Triangular(min_val=1.0, mode=3.0, max_val=5.0)
        assert dist.min_val == 1.0
        assert dist.mode == 3.0
        assert dist.max_val == 5.0

    def test_init_equal_values(self):
        """모든 값이 같은 경우 테스트"""
        dist = Triangular(min_val=2.0, mode=2.0, max_val=2.0)
        assert dist.min_val == 2.0
        assert dist.mode == 2.0
        assert dist.max_val == 2.0

    def test_init_mode_equals_min(self):
        """mode가 min과 같은 경우 테스트"""
        dist = Triangular(min_val=1.0, mode=1.0, max_val=5.0)
        assert dist.min_val == 1.0
        assert dist.mode == 1.0
        assert dist.max_val == 5.0

    def test_init_mode_equals_max(self):
        """mode가 max와 같은 경우 테스트"""
        dist = Triangular(min_val=1.0, mode=5.0, max_val=5.0)
        assert dist.min_val == 1.0
        assert dist.mode == 5.0
        assert dist.max_val == 5.0

    def test_init_invalid_min_greater_than_mode(self):
        """min > mode인 경우 ValueError 발생 테스트"""
        with pytest.raises(ValueError, match="Condition min_val <= mode <= max_val must be met"):
            Triangular(min_val=5.0, mode=3.0, max_val=7.0)

    def test_init_invalid_mode_greater_than_max(self):
        """mode > max인 경우 ValueError 발생 테스트"""
        with pytest.raises(ValueError, match="Condition min_val <= mode <= max_val must be met"):
            Triangular(min_val=1.0, mode=6.0, max_val=5.0)

    def test_init_invalid_min_greater_than_max(self):
        """min > max인 경우 ValueError 발생 테스트"""
        with pytest.raises(ValueError, match="Condition min_val <= mode <= max_val must be met"):
            Triangular(min_val=7.0, mode=5.0, max_val=3.0)

    def test_generate_returns_float(self):
        """generate 메서드가 float 타입을 반환하는지 테스트"""
        dist = Triangular(min_val=0.0, mode=1.0, max_val=2.0)
        result = dist.generate()
        assert isinstance(result, float)

    def test_generate_within_range(self):
        """생성된 값이 범위 내에 있는지 테스트"""
        min_val, mode, max_val = 2.0, 5.0, 8.0
        dist = Triangular(min_val=min_val, mode=mode, max_val=max_val)

        # 충분한 샘플 생성하여 범위 확인
        for _ in range(1000):
            value = dist.generate()
            assert min_val <= value <= max_val

    def test_generate_statistical_properties(self):
        """생성된 값들의 통계적 특성 테스트"""
        min_val, mode, max_val = 0.0, 4.0, 10.0
        dist = Triangular(min_val=min_val, mode=mode, max_val=max_val)

        # 충분한 샘플 생성
        samples = [dist.generate() for _ in range(10000)]

        # 삼각분포의 평균: (min + mode + max) / 3
        expected_mean = (min_val + mode + max_val) / 3
        sample_mean = np.mean(samples)
        assert abs(sample_mean - expected_mean) < 0.2

        # 모든 값이 범위 내에 있는지 확인
        assert all(min_val <= sample <= max_val for sample in samples)

    def test_repr(self):
        """__repr__ 메서드 테스트"""
        dist = Triangular(min_val=1.0, mode=2.5, max_val=4.0)
        expected = "Triangular(min_val=1.0, mode=2.5, max_val=4.0)"
        assert repr(dist) == expected
    # mode == max_val
    tri2 = Triangular(0.0, 10.0, 10.0)
    assert tri2.mode == tri2.max_val == 10.0

    # 모든 값이 같은 경우
    tri3 = Triangular(5.0, 5.0, 5.0)
    assert tri3.min_val == tri3.mode == tri3.max_val == 5.0


def test_triangular_generate_range():
    """Triangular 분포 생성값이 범위 내에 있는지 테스트"""
    tri = Triangular(2.0, 7.0, 12.0)

    for _ in range(1000):
        value = tri.generate()
        assert 2.0 <= value <= 12.0


@pytest.mark.parametrize("min_value, mode, max_value", [(0.0, 50.0, 100.0)])
def test_triangular_generate_mode_preference(min_value: float, mode: float, max_value: float):
    """Triangular 분포가 mode 값 주변에 더 많은 샘플을 생성하는지 테스트"""
    tri = Triangular(min_value, mode, max_value)
    samples = [tri.generate() for _ in range(10000)]

    # mode 근처(40-60)에 더 많은 샘플이 있어야 함
    near_mode = sum(1 for s in samples if 40.0 <= s <= 60.0)
    far_from_mode = sum(1 for s in samples if s <= 20.0 or s >= 80.0)

    assert near_mode > far_from_mode


def test_triangular_repr():
    """__repr__ 메서드 테스트"""
    tri = Triangular(1.0, 2.5, 4.0)
    assert repr(tri) == "Triangular(min_val=1.0, mode=2.5, max_val=4.0)"
