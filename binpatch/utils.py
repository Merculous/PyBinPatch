
from .errors import EmptyError, ZeroError, NotEqualError
from .types import Buffer, WritableBuffer, Index, Size


def getBufferAtIndex(data: Buffer, index: Index, length: Size) -> Buffer:
    if not isinstance(data, Buffer):
        raise TypeError('Data must be of type: Buffer')

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


def replaceBufferAtIndex(data: WritableBuffer, pattern: Buffer, index: Index, length: Size) -> WritableBuffer:
    if not isinstance(data, WritableBuffer):
        raise TypeError('Data must be of type: WritableBuffer')

    buffer = getBufferAtIndex(data, index, length)

    if buffer == pattern:
        return data

    data[index:index+length] = pattern

    patchedBuffer = getBufferAtIndex(data, index, length)

    if patchedBuffer != pattern:
        raise ValueError('Failed to replace buffer!')

    return data
