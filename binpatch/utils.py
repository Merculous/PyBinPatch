
from .errors import EmptyError, ZeroError, NotEqualError
from .types import Index, Size, ReadOnlyBuffer, WritableBuffer


def getBufferAtIndex(data: ReadOnlyBuffer, index: Index, length: Size) -> ReadOnlyBuffer:
    if not isinstance(data, ReadOnlyBuffer):
        raise TypeError('Data must be of type: ReadOnlyBuffer')

    if not data:
        raise EmptyError('Data is empty!')

    if not isinstance(index, Index):
        raise TypeError('Index must be of type: Index')

    if index not in range(len(data)):
        raise IndexError(f'Bad index: {index}')

    if not isinstance(length, Size):
        raise TypeError('Length must be of type: Size')

    if length == 0:
        raise ZeroError('Length must not be 0!')

    buffer = data[index:index+length]

    if not buffer:
        raise EmptyError('Buffer is empty!')

    buffer_len = len(buffer)

    if buffer_len != length:
        raise NotEqualError(f'Buffer length mismatch! Got {buffer_len}')

    return buffer


def replaceBufferAtIndex(data: WritableBuffer, pattern: WritableBuffer, index: Index, length: Size) -> WritableBuffer:
    if not isinstance(data, WritableBuffer):
        raise TypeError('Data must be of type: WritableBuffer')

    if not isinstance(pattern, WritableBuffer):
        raise TypeError('Pattern must be of type: WritableBuffer')

    if len(pattern) != length:
        raise NotEqualError('Pattern must be the same size as length!')

    buffer = getBufferAtIndex(data, index, length)

    if buffer == pattern:
        return data

    data[index:index+length] = pattern

    patchedBuffer = getBufferAtIndex(data, index, length)

    if patchedBuffer != pattern:
        raise ValueError('Failed to replace buffer!')

    return data
