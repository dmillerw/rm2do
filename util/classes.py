from dataclasses import dataclass
from typing import Dict, List, Self

from dataclasses_json import DataClassJsonMixin


@dataclass
class XYCoordinate(DataClassJsonMixin):
    x: int
    y: int

    def within_bounds(self, a: Self, b: Self) -> bool:
        min_x = min(a.x, b.x)
        min_y = min(a.y, b.y)
        max_x = max(a.x, b.x)
        max_y = max(a.y, b.y)

        return min_x <= self.x <= max_x and min_y <= self.y <= max_y


@dataclass
class TaskCoordinates(DataClassJsonMixin):
    id: str
    start: XYCoordinate
    end: XYCoordinate


@dataclass
class TaskData(DataClassJsonMixin):
    pages: Dict[int, List[TaskCoordinates]]


@dataclass
class GoogleTask:
    id: str
    parent: str | None
    title: str
    status: str
