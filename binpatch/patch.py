
from binpatch.errors import NotEqualError
from .types import ReadOnlyBuffer, Differences
from .utils import getBufferAtIndex, replaceBufferAtIndex


def patchFromDifferences(data: ReadOnlyBuffer, differences: Differences) -> ReadOnlyBuffer:
    if not isinstance(data, ReadOnlyBuffer):
        raise TypeError('Data must be of type: ReadOnlyBuffer')

    patched = bytearray(data)

    for difference in differences:
        buffer = getBufferAtIndex(patched, difference.index, difference.size)

        if buffer != difference.a:
            raise NotEqualError('A attribute not the same!')

        patched = replaceBufferAtIndex(patched, difference.b, difference.index, difference.size)

    return bytes(patched)
