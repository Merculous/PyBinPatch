
from binascii import hexlify
from difflib import SequenceMatcher

from .file import readFuzzyPatcherJSON
from .utils import timer


@timer
def findPattern(pattern: bytes, data: bytes):
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
def findPatternsFromFuzzyJSON(jsonPath: str, data: bytes) -> None:
    fuzzy = readFuzzyPatcherJSON(jsonPath)
    patterns = [f.pattern for f in fuzzy]

    for patternCounter, pattern in enumerate(patterns, 1):
        ratio, i = findPattern(pattern, data)
        patternStr = hexlify(pattern).decode()

        print(f'[{patternCounter}/{len(patterns)}]')
        print(f'Pattern: {patternStr}')
        print(f'Size: {len(pattern)}')
        print(f'{ratio}% 0x{i:x}')
