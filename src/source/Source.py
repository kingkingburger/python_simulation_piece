from dataclasses import dataclass
from enum import Enum

from entity.Entity import Entity


class PullPushMode(Enum):
    """
    Push: 다음 컴포넌트의 상태와 무관하게 개체를 전달.
    Pull: 다음 컴포넌트가 받을 준비가 되었을 때만 전달.
    """
    PUSH = "PUSH"
    PULL = "PULL"


@dataclass
class Source:
    entityType: Entity
    arriveTime: float
    arriveCount: int
    maxArriveCount: int
    mode: PullPushMode

