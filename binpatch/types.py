
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass
class Difference:
    a: Sequence
    b: Sequence
    offset: int
    size: int


Differences = list[Difference]
