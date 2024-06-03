
import json
from typing import Any


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
