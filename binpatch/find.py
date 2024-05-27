
from binascii import hexlify
from difflib import SequenceMatcher
from typing import Optional

from .file import readFuzzyPatcherJSON
from .utils import timer


@timer
def findPattern(
    pattern: bytes,
    data: bytes,
    hashes: Optional[set] = None,
    prevPattern: Optional[bytes] = None
) -> tuple:

    patternSize = len(pattern)
    dataSize = len(data)

    if not isinstance(hashes, set):
        hashes = set()

    matcher = SequenceMatcher()
    matcher.set_seq2(pattern)

    matches = []

    for i in range(dataSize - patternSize + 1):
        buff = data[i:i+patternSize]
        buffHash = hash(buff)

        if all((buffHash in hashes, any((prevPattern is None, prevPattern == pattern)))):
            continue

        hashes.add(buffHash)

        matcher.set_seq1(buff)
        ratio = matcher.quick_ratio()

        if ratio == 0:
            continue

        match = (round(ratio * 100, 2), i)
        matches.append(match)

    return matches, hashes, pattern


@timer
def findPatternsFromFuzzyJSON(jsonPath: str, data: bytes) -> None:
    fuzzy = readFuzzyPatcherJSON(jsonPath)
    hashTable = set()
    prevPattern = None

    for i, fuzz in enumerate(fuzzy, 1):
        pattern = fuzz.pattern
        matches, hashes, prevPattern = findPattern(pattern, data, hashTable, prevPattern)
        hashTable.update(hashes)

        matches = sorted(matches, reverse=True)[:10]

        print(f'Hashes: {len(hashTable)}')
        print(f'[{i}/{len(fuzzy)}]')
        print(f'Pattern: {len(pattern)} {hexlify(pattern).decode()}')

        for match, offset in matches:
            print(f'{match}% 0x{offset:x}')
