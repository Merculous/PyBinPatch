
from dataclasses import dataclass


@dataclass
class Difference:
    offset: int
    size: int
    orig: bytes
    new: bytes
