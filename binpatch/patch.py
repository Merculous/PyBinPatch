
from .diff import Difference
from .errors import SizeMismatch


def applyPatchAtOffset(
        offset: int,
        size: int,
        orig: bytes,
        new: bytes,
        data: bytearray
) -> None:

    if any((len(orig) != size, len(new) != size)):
        raise SizeMismatch(f'Patches are not of size {size}!')

    origCheck = data[offset:offset+size]

    if origCheck != orig:
        raise Exception('Original data does not match!')

    data[offset:offset+size] = new


def applyPatchesFromDifferences(diffs: list[Difference], data: bytes) -> bytes:
    buffer = bytearray(data)

    for diff in diffs:
        sliceCheck = data[diff.offset:diff.offset+diff.size]

        if diff.orig != sliceCheck:
            raise Exception(f'0x{diff.offset:x} orig data does not match!')

        applyPatchAtOffset(diff.offset, diff.size, diff.orig, diff.new, buffer)

    return bytes(buffer)
