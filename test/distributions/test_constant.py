import pytest
from src.distributions.constant import Constant


def test_constant_initialization():
    """Constant 분포 초기화 테스트"""
    const = Constant(5.0)
    assert const.value == 5.0

    const_int = Constant(10)
    assert const_int.value == 10


def test_constant_generate():
    """Constant 분포 생성 테스트"""
    const = Constant(3.14)
    for _ in range(100):
        assert const.generate() == 3.14


def test_constant_generate_returns_float():
    """generate 메서드가 항상 float를 반환하는지 테스트"""
    const = Constant(42)
    result = const.generate()
    assert isinstance(result, float)
    assert result == 42.0


def test_constant_repr():
    """__repr__ 메서드 테스트"""
    const = Constant(2.5)
    assert repr(const) == "Constant(value=2.5)"
