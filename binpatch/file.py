
import json
from typing import Iterable


def readDataFromPath(path: str) -> bytes:
    with open(path, 'rb') as f:
        return f.read()


def readJSONFromPath(path: str) -> Iterable:
    with open(path) as f:
        return json.load(f)


def writeJSONToPath(path: str, data: Iterable, *args, **kwargs) -> None:
    with open(path, 'w') as f:
        json.dump(data, f, *args, **kwargs)
