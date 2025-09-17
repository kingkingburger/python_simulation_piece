from datetime import datetime


class Item:
    """창고에 저장되는 개체를 나타내는 클래스"""

    def __init__(self, id: str, name: str, priority: int = 0, storage_cost: float = 0.01):
        self.id = id
        self.name = name
        self.priority = priority
        self.storage_cost = storage_cost  # 보관 비용
        self.created_at = datetime.now()
