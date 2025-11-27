
import json
from pathlib import Path
from typing import Any


def readBytesFromPath(path: Path) -> bytes:
    if not isinstance(path, Path):
        raise TypeError(f'Path must be of type: {Path}')

    if not path.is_file():
        raise TypeError('Path must be a file!')

    return path.read_bytes()


def writeBytesToPath(path: Path, data: bytes) -> int:
    if not isinstance(path, Path):
        raise TypeError(f'Path must be of type: {Path}')

    if path.is_file():
        raise FileExistsError('Path exists! Not overwriting!')

    return path.write_bytes(data)


def readDataFromJSONFile(path: Path) -> Any:
    if not isinstance(path, Path):
        raise TypeError(f'Path must be of type: {Path}')

    if not path.is_file():
        raise TypeError('Path must be a file!')

    with path.open() as f:
        return json.load(f)


def writeDataToJSONFile(path: Path, data: Any, indent: int = 2) -> None:
    if not isinstance(path, Path):
        raise TypeError(f'Path must be of type: {Path}')

    if path.is_file():
        raise FileExistsError('Path exists! Not overwriting!')

    with path.open('w') as f:
        json.dump(data, f, indent=indent)
