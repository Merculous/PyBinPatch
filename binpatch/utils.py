
from collections.abc import MutableSequence, Sequence


def getBufferAtIndex(data: Sequence, index: int, length: int) -> Sequence:
    if not isinstance(data, Sequence):
        raise TypeError(f'Data must be of type: {Sequence}')

    if not data:
        raise ValueError('Data is empty!')

    if not isinstance(index, int):
        raise TypeError('Index must be of type: int')

    dataSize = len(data)

    if index not in range(dataSize):
        raise IndexError(f'Bad index: {index}')

    if not isinstance(length, int):
        raise TypeError('Length must be of type: int')

    if length == 0:
        raise ValueError('Length must not be 0!')
    
    if index + length > dataSize:
        raise IndexError('Index overflow!')

    window = data[index:index+length]

    if not window:
        raise ValueError('Buffer is empty!')

    windowSize = len(window)

    if windowSize != length:
        raise ValueError(f'Buffer length mismatch! Got {windowSize}')

    return window


def replaceBufferAtIndex(data: MutableSequence, pattern: Sequence, index: int, length: int) -> MutableSequence:
    if not isinstance(data, MutableSequence):
        raise TypeError(f'Data must be of type: {MutableSequence}')

    if not isinstance(pattern, Sequence):
        raise TypeError(f'Pattern must be of type: {Sequence}')

    if not isinstance(index, int):
        raise TypeError('Index must be an int!')

    if not isinstance(length, int):
        raise TypeError('Length must be an int!')

    if length == 0:
        raise ValueError('Length cannot be 0!')

    dataSize = len(data)

    if dataSize < length:
        raise ValueError(f'Data must be at least {length} bytes or bigger!')

    patternSize = len(pattern)

    if patternSize != length:
        raise ValueError('Pattern must be the same size as length!')

    window = getBufferAtIndex(data, index, length)

    if window == pattern:
        return data

    data[index:index+length] = pattern
    return data
