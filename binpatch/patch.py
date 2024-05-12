
from .diff import Difference


def applyPatchesFromDifferences(differences: list[Difference], data: bytes) -> bytes:
    buffer = bytearray(data)

    for diff in differences:
        sliceCheck = data[diff.offset:diff.offset+diff.size]

        if diff.orig != sliceCheck:
            raise Exception(f'0x{diff.offset:x} orig data does not match!')

        buffer[diff.offset:diff.offset+diff.size] = diff.new

    return buffer
