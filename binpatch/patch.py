
from collections.abc import MutableSequence

from .types import Differences
from .utils import getBufferAtIndex, replaceBufferAtIndex


def patchFromDifferences(data: MutableSequence, differences: Differences) -> MutableSequence:
    if not isinstance(data, MutableSequence):
        raise TypeError(f'Data must be of type: {MutableSequence}')

    for difference in differences:
        buffer = getBufferAtIndex(data, difference.offset, difference.size)

        if buffer != difference.a:
            raise ValueError('A attribute not the same!')

        data = replaceBufferAtIndex(data, difference.b, difference.offset, difference.size)

    return data
