import math
from dataclasses import dataclass


@dataclass
class Vec:
    x: float = 0
    y: float = 0

    def abs(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __add__(self, other: 'Vec') -> 'Vec':
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vec') -> 'Vec':
        return Vec(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vec':
        return Vec(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> 'Vec':
        return Vec(self.x / scalar, self.y / scalar)

    def is_close_to(self, other: 'Vec', eps = 1.0) -> bool:
        return (self-other).abs() < eps


@dataclass
class Entity:
    pos: Vec
    v: Vec
    radius: float


@dataclass
class Field:
    w: float # x
    h: float # y

    # assume centered goals
    # TODO: measure goal position
    home_goal_height: float
    opponent_goal_height: float
    # TODO: round corners
