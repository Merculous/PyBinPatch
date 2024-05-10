
from binascii import hexlify
from dataclasses import asdict

from .errors import SizeMismatch
from .file import writeJSONToPath
from .types import Difference


def findDifferences(orig_data: bytes, patched_data: bytes) -> list[Difference]:
    orig_size = len(orig_data)
    patched_size = len(patched_data)

    if orig_size != patched_size:
        raise SizeMismatch(f'Original: {orig_size}, Patched: {patched_size}')

    offset = 0
    origBuff = b''
    patchedBuff = b''

    differences = []

    for i, (v1, v2) in enumerate(zip(orig_data, patched_data)):
        if v1 == v2:
            continue

        v1 = v1.to_bytes(1)
        v2 = v2.to_bytes(1)

        if offset == 0:
            offset += i
            origBuff += v1
            patchedBuff += v2
            continue

        elif offset + 1 == i:
            offset += 1
            origBuff += v1
            patchedBuff += v2
            continue

        else:
            origBuffLen = len(origBuff)
            patchedBuffLen = len(patchedBuff)

            if origBuffLen != patchedBuffLen:
                raise SizeMismatch('An error occurred during diff buffers!')

            diff = Difference(offset, origBuffLen, origBuff, patchedBuff)
            differences.append(diff)

            origBuff = v1
            patchedBuff = v2
            offset = i

    return differences


def printDifferences(differences: list[Difference]) -> None:
    for diff in differences:
        print(f'Offset: {diff.offset:x}')
        print(f'Size: {diff.size:x}')
        print(f'Original: {hexlify(diff.orig).decode("utf-8")}')
        print(f'Patched: {hexlify(diff.new).decode("utf-8")}')


def serializeDifference(difference: Difference) -> dict:
    diff = difference
    diff.orig = hexlify(diff.orig).decode('utf-8')
    diff.new = hexlify(diff.new).decode('utf-8')
    diff = asdict(diff)
    return diff


def diffToJSONFile(orig_data: bytes, patched_data: bytes, path: str) -> None:
    differences = findDifferences(orig_data, patched_data)
    serialized = [serializeDifference(d) for d in differences]
    writeJSONToPath(path, serialized, indent=2)
