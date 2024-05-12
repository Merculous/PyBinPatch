
from binascii import hexlify
from dataclasses import dataclass, asdict

from .errors import SizeMismatch
from .file import writeJSONToPath, readJSONFromPath


@dataclass
class Difference:
    offset: int
    size: int
    orig: bytes
    new: bytes


def findDifferences(orig_data: bytes, patched_data: bytes) -> list[Difference]:
    orig_size = len(orig_data)
    patched_size = len(patched_data)

    if orig_size != patched_size:
        raise SizeMismatch(f'Original: {orig_size}, Patched: {patched_size}')

    start = 0
    stop = 0
    origBuff = b''
    patchedBuff = b''

    differences = []

    for i, (v1, v2) in enumerate(zip(orig_data, patched_data)):
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

            diff = Difference(start, buffSize, origBuff, patchedBuff)
            differences.append(diff)

            start = i
            stop = i
            origBuff = v1
            patchedBuff = v2

    if all((origBuff, patchedBuff, start <= stop)):
        # Last
        buffSize = len(origBuff)
        diff = Difference(start, buffSize, origBuff, patchedBuff)
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
    return diff


def diffToJSONFile(orig_data: bytes, patched_data: bytes, path: str) -> None:
    differences = findDifferences(orig_data, patched_data)
    serialized = [serializeDifference(d) for d in differences]
    writeJSONToPath(path, serialized, indent=2)


def readDifferencesFromJSONFile(path: str) -> list[Difference]:
    data = readJSONFromPath(path)

    differences = []

    for diff in data:
        diff['orig'] = bytes.fromhex(diff['orig'])
        diff['new'] = bytes.fromhex(diff['new'])

        difference = Difference(*diff.values())
        differences.append(difference)

    return differences
