
from dataclasses import dataclass
from pathlib import Path

Buffer = bytes | bytearray | str
ReadOnlyBuffer = bytes | str
WritableBuffer = bytearray
Index = int
Size = int
FilesystemPath = Path
Matches = list[Index]


@dataclass
class Difference:
    a: Buffer
    b: Buffer
    size: Size
    index: Index


Differences = list[Difference]
Percentage = float
SimilarMatches = list[tuple[Matches, Percentage]]
