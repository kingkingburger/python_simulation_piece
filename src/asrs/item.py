from datetime import datetime


class Item:
    """창고에 저장되는 개체를 나타내는 클래스"""

    def __init__(self, id: str, name: str, priority: int = 0):
        self.id = id
        self.name = name
        self.priority = priority
        self.created_at = datetime.now()
