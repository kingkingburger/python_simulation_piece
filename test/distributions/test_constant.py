from src.distributions.constant import Constant
import pytest
from src.distributions.constant import Constant


class TestConstant:
    """Constant 분포 테스트 클래스"""

    def test_init_with_integer(self):
        """정수 값으로 초기화 테스트"""
        dist = Constant(10)
        assert dist.value == 10

    def test_init_with_float(self):
        """실수 값으로 초기화 테스트"""
        dist = Constant(3.14)
        assert dist.value == 3.14

    def test_generate_returns_constant_value(self):
        """generate 메서드가 항상 같은 값을 반환하는지 테스트"""
        value = 42
        dist = Constant(value)

        # 여러 번 호출해도 같은 값을 반환해야 함
        for _ in range(100):
            assert dist.generate() == float(value)

    def test_generate_returns_float(self):
        """generate 메서드가 float 타입을 반환하는지 테스트"""
        dist = Constant(5)
        result = dist.generate()
        assert isinstance(result, float)

    def test_repr(self):
        """__repr__ 메서드 테스트"""
        dist = Constant(7.5)
        expected = "Constant(value=7.5)"
        assert repr(dist) == expected

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
