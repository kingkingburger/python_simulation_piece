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
import pytest
from src.distributions.base import Distribution


class TestDistribution:
    """Distribution 추상 클래스 테스트"""

    def test_cannot_instantiate_abstract_class(self):
        """추상 클래스를 직접 인스턴스화할 수 없는지 테스트"""
        with pytest.raises(TypeError):
            Distribution()

    def test_subclass_must_implement_generate(self):
        """서브클래스가 generate 메서드를 구현해야 하는지 테스트"""

        class IncompleteDistribution(Distribution):
            pass

        with pytest.raises(TypeError):
            IncompleteDistribution()

    def test_valid_subclass_implementation(self):
        """올바른 서브클래스 구현 테스트"""

        class ValidDistribution(Distribution):
            def generate(self) -> float:
                return 42.0

        # 인스턴스 생성이 성공해야 함
        dist = ValidDistribution()
        assert dist.generate() == 42.0
        assert isinstance(dist, Distribution)
    with pytest.raises(TypeError):
        IncompleteDistribution()


def test_distribution_subclass_with_generate_works():
    """generate 메서드를 구현한 서브클래스는 정상 작동"""

    class TestDistribution(Distribution):
        def generate(self) -> float:
            return 42.0

    dist = TestDistribution()
    assert dist.generate() == 42.0
