import pytest
from src.distributions.base import Distribution


def test_distribution_is_abstract():
    """Distribution이 추상 클래스인지 확인"""
    with pytest.raises(TypeError):
        Distribution()


def test_distribution_subclass_must_implement_generate():
    """Distribution을 상속받은 클래스는 generate 메서드를 구현해야 함"""

    class IncompleteDistribution(Distribution):
        pass

    with pytest.raises(TypeError):
        IncompleteDistribution()


def test_distribution_subclass_with_generate_works():
    """generate 메서드를 구현한 서브클래스는 정상 작동"""

    class TestDistribution(Distribution):
        def generate(self) -> float:
            return 42.0

    dist = TestDistribution()
    assert dist.generate() == 42.0
