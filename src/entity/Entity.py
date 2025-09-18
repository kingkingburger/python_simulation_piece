from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Entity:
    name: str
    width: float
    length: float
    height: float
    weight: float
    order: int
    tag: Dict[str, str] = field(default_factory=dict)

