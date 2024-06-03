
from binascii import hexlify
from difflib import SequenceMatcher

from .diff import Difference
from .utils import timer


@timer
def findPattern(pattern: bytes, data: bytes) -> list:
    patternSize = len(pattern)
    dataSize = len(data)
    readSize = dataSize - patternSize + 1

    matcher = SequenceMatcher()
    matcher.set_seq2(pattern)

    buffers = {}

    for i in range(readSize):
        buffer = data[i:i+patternSize]
        bufferHash = hash(buffer)

        if bufferHash in buffers:
            continue

        matcher.set_seq1(buffer)
        ratio = matcher.quick_ratio()

        if ratio == 0:
            continue

        buffers[bufferHash] = {i: round(ratio * 100, 2)}

    ratios = []

    for buffHash in buffers:
        for i, ratio in buffers[buffHash].items():
            if ratio in ratios:
                continue

            ratios.append(ratio)

    ratiosSorted = sorted(ratios, reverse=True)
    bestRatio = ratiosSorted[0]
    bestMatch = []

    for buffHash in buffers:
        if bestMatch:
            break

        for i, ratio in buffers[buffHash].items():
            if ratio != bestRatio:
                continue

            bestMatch.extend((ratio, i))

    return bestMatch


@timer
def findPatternsFromDifferences(differences: list[Difference], data: bytes) -> None:
    nPatterns = len(differences)
    exactMatches = 0

    for patternCounter, difference in enumerate(differences, 1):
        ratio, i = findPattern(difference.pattern, data)
        patternStr = hexlify(difference.pattern).decode()

        if ratio == 100:
            exactMatches += 1

        print(f'[{patternCounter}/{nPatterns}]')
        print(f'Pattern: {patternStr}')
        print(f'Size: {len(difference.pattern)}')
        print(f'Match: {ratio}%')
        print(f'Offset: 0x{i:x}')

    print(f'Exact matches: {exactMatches}/{nPatterns}')
