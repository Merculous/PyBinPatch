
from binascii import hexlify
from collections.abc import Sequence
from pathlib import Path

from binpatch.utils import getBufferAtIndex

from .io import readDataFromJSONFile, writeDataToJSONFile
from .types import Difference, Differences


def diff(a: Sequence, b: Sequence) -> Differences:
    if not isinstance(a, Sequence):
        raise TypeError(f'A must be of type: {Sequence}')

    if not isinstance(b, Sequence):
        raise TypeError(f'B must be of type: {Sequence}')

    aSize = len(a)
    bSize = len(b)

    if aSize != bSize:
        raise ValueError(f'Size mismatch: a: {aSize}, b: {bSize}')

    differenceStart = -1
    differenceSize = 0

    differences = []

    for i in range(aSize + 1):
        if i == aSize or a[i] == b[i]:
            if differenceStart >= 0 and differenceSize >= 1:
                difference = Difference(
                    getBufferAtIndex(a, differenceStart, differenceSize),
                    getBufferAtIndex(b, differenceStart, differenceSize),
                    differenceStart,
                    differenceSize
                )

                differences.append(difference)

                differenceStart = -1
                differenceSize = 0

                continue
            else:
                continue

        if differenceStart == -1:
            differenceStart = i
            differenceSize += 1
            continue

        if differenceStart + differenceSize == i:
            differenceSize += 1
            continue

    return differences


def diffToJSONFile(a: Sequence, b: Sequence, path: Path) -> None:
    if not isinstance(a, Sequence):
        raise TypeError(f'a must be of type: {Sequence}')

    if not isinstance(b, Sequence):
        raise TypeError(f'a must be of type: {Sequence}')

    if not isinstance(path, Path):
        raise TypeError(f'Path must be of type: {Path}')

    differences = diff(a, b)
    differencesJSON = {}

    for difference in differences:
        differencesJSON[hex(difference.offset)] = {
            'a': hexlify(difference.a).decode(),
            'b': hexlify(difference.b).decode(),
            'size': hex(difference.size)
        }

    writeDataToJSONFile(path, differencesJSON)


def readDifferencesJSONFile(path: Path) -> Differences:
    if not isinstance(path, Path):
        raise TypeError(f'Path must be of type: {Path}')

    differencesJSON = readDataFromJSONFile(path)
    differences = []

    for offset in differencesJSON:
        info = differencesJSON[offset]

        difference = Difference(
            b''.fromhex(info['a']),
            b''.fromhex(info['b']),
            int(offset, 16),
            int(info['size'], 16)
        )

        differences.append(difference)

    return differences
