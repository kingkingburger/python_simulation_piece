from dataclasses import dataclass


@dataclass
class Entity:
    name: str
    width: float
    length: float
    height: float
    weight: float
    order: int
    tag: str

