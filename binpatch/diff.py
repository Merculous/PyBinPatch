
from binascii import hexlify
from dataclasses import dataclass, asdict

from .errors import SizeMismatch
from .file import writeJSONToPath, readJSONFromPath


@dataclass
class Difference:
    offset: int
    patchOffset: int
    size: int
    orig: bytes
    new: bytes
    patternSize: int
    pattern: bytes


def initPattern(data: bytes, offset: int, buffSize: int, expandSize: int = 8) -> tuple:
    pattern = data[offset-buffSize-expandSize:offset+buffSize+expandSize]
    patternSize = len(pattern)
    patternOffset = patternSize - expandSize - buffSize
    return pattern, patternSize, patternOffset


def findDifferences(origData: bytes, patchedData: bytes) -> list[Difference]:
    orig_size = len(origData)
    patched_size = len(patchedData)

    if orig_size != patched_size:
        raise SizeMismatch(f'Original: {orig_size}, Patched: {patched_size}')

    start = 0
    stop = 0
    origBuff = b''
    patchedBuff = b''

    differences = []

    for i, (v1, v2) in enumerate(zip(origData, patchedData)):
        if v1 == v2:
            continue

        v1 = v1.to_bytes(1)
        v2 = v2.to_bytes(1)

        if all((start == 0, stop == 0)):
            # First
            start += i
            stop += i

            origBuff += v1
            patchedBuff += v2
            continue

        elif all((start <= stop, stop + 1 == i)):
            stop += 1

            origBuff += v1
            patchedBuff += v2
            continue

        else:
            buffSize = len(origBuff)

            pattern, patternSize, patternOffset = initPattern(origData, start, buffSize)

            diff = Difference(
                start,
                patternOffset,
                buffSize,
                origBuff,
                patchedBuff,
                patternSize,
                pattern
            )

            differences.append(diff)

            start = i
            stop = i
            origBuff = v1
            patchedBuff = v2

    if all((origBuff, patchedBuff, start <= stop)):
        # Last
        buffSize = len(origBuff)

        pattern, patternSize, patternOffset = initPattern(origData, start, buffSize)

        diff = Difference(
            start,
            patternOffset,
            buffSize,
            origBuff,
            patchedBuff,
            patternSize,
            pattern
        )

        differences.append(diff)

    return differences


def printDifferences(differences: list[Difference]) -> None:
    for diff in differences:
        print(f'Offset: {diff.offset:x}')
        print(f'Size: {diff.size:x}')
        print(f'Original: {hexlify(diff.orig).decode("utf-8")}')
        print(f'Patched: {hexlify(diff.new).decode("utf-8")}')


def serializeDifference(difference: Difference) -> dict:
    diff = asdict(difference)
    diff['orig'] = hexlify(diff['orig']).decode('utf-8')
    diff['new'] = hexlify(diff['new']).decode('utf-8')
    diff['pattern'] = hexlify(diff['pattern']).decode('utf-8')
    return diff


def unserializeDifference(difference: dict) -> Difference:
    difference['orig'] = b''.fromhex(difference['orig'])
    difference['new'] = b''.fromhex(difference['new'])
    difference['pattern'] = b''.fromhex(difference['pattern'])
    return Difference(*difference.values())


def diffToJSONFile(origData: bytes, patchedData: bytes, path: str) -> None:
    differences = findDifferences(origData, patchedData)
    serialized = [serializeDifference(d) for d in differences]
    writeJSONToPath(path, serialized, indent=2)


def readDifferencesFromJSONFile(path: str) -> list[Difference]:
    jsonData = readJSONFromPath(path)
    differences = [unserializeDifference(d) for d in jsonData]
    return differences
