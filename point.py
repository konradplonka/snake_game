from __future__ import annotations
from dataclasses import dataclass
from config import Config

@dataclass
class Point:
    x: int
    y: int

    def __eq__(self, other: Point) -> bool:
        if type(other) != Point:
            raise TypeError('Wrong object type to comparison!')
        if other.x == self.x and other.y == self.y:
            return True
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __sub__(self, other: Point) -> Point:
        if type(other) != Point:
            raise TypeError('Wrong object type to substract operation!')
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other: Point) -> Point:
        if type(other) != Point:
            raise TypeError('Wrong object type to add operation!')
        return Point(self.x + other.x, self.y + other.y)



