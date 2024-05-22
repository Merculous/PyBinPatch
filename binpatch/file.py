
import json
from dataclasses import dataclass
from typing import Any


@dataclass
class FuzzyDiff:
    offset: int
    size: int
    orig: bytes
    new: bytes
    patternSize: int
    pattern: bytes


def readDataFromPath(path: str) -> bytes:
    with open(path, 'rb') as f:
        return f.read()


def readJSONFromPath(path: str) -> Any:
    with open(path) as f:
        return json.load(f)


def writeJSONToPath(path: str, data: Any, *args, **kwargs) -> None:
    with open(path, 'w') as f:
        json.dump(data, f, *args, **kwargs)


def writeDataToPath(path: str, data: bytes) -> None:
    with open(path, 'wb') as f:
        f.write(data)


def readFuzzyPatcherJSON(path: str) -> list[FuzzyDiff]:
    data = readJSONFromPath(path)
    diffs = []

    for patch in data['patches']:
        start = int(patch['patchOffset'], 16)
        pattern = b''.fromhex(patch['patternBytes'])
        offset = int(patch['comment'].split()[-1], 16)
        new = b''.fromhex(patch['patchBytes'])
        orig = pattern[start:start+len(new)]

        diff = FuzzyDiff(
            offset,
            len(new),
            orig,
            new,
            len(pattern),
            pattern
        )

        diffs.append(diff)

    return diffs
