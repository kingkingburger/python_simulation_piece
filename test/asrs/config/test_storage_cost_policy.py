from pytest import approx

from src.asrs.asrs import ASRS
from src.asrs.config.storage_cost_policy import StorageCostPolicy
from src.asrs.item import Item
from src.asrs.position import Position


class TestStorageCostPolicy:
    def test_item_with_storage_cost(self):
        # given
        item = Item("item1", "테스트 아이템", storage_cost=0.02)

        # when & then
        assert item.storage_cost == 0.02
        assert item.id == "item1"
        assert item.name == "테스트 아이템"

    def test_item_default_storage_cost(self):
        # given
        item = Item("item1", "테스트 아이템")

        # when & then
        assert item.storage_cost == 0.01  # 기본값 확인

    def test_asrs_default_per_item_policy(self):
        # given
        asrs = ASRS(max_x=2, max_y=2, max_z=2)

        # when & then
        assert asrs.storage_cost_policy == StorageCostPolicy.PER_TIME_UNIT
        assert asrs.cost == 0.01  # 기본 비용율 확인

    def test_asrs_calculate_storage_cost_with_per_item(self):
        # given
        asrs = ASRS(max_x=2, max_y=2, max_z=2, storage_cost_policy=StorageCostPolicy.PER_TIME_UNIT)
        item_count = 3

        # when
        total_cost = asrs.calculate_storage_cost(item_count)

        # then
        # 3개 * 0.01 = 0.15
        expected_cost = 0.03
        assert total_cost == approx(expected_cost)

    def test_asrs_calculate_total_storage_cost(self):
        # given
        asrs = ASRS(max_x=2, max_y=2, max_z=1,
                   storage_cost_policy=StorageCostPolicy.PER_TIME_UNIT,
                   cost_time=1.0)  # 1초

        # 아이템들 추가
        item1 = Item("1", "아이템1")
        item2 = Item("2", "아이템2")
        item3 = Item("3", "아이템3")

        asrs.put_item(item1, Position(0, 0, 0))
        asrs.put_item(item2, Position(1, 0, 0))
        asrs.put_item(item3, Position(0, 1, 0))

        # when
        total_cost = asrs.calculate_total_storage_cost(0.01)

        # then
        # 각 셀마다: 1초 * 0.01 * 1개 = 0.01
        # 3개 셀: 0.01 * 3 = 0.03
        expected_cost = 0.03
        assert total_cost == approx(expected_cost)