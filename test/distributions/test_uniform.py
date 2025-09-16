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
