
import re
from difflib import SequenceMatcher

from .utils import getDataAtOffset


def lookForPatternWithExactMatches(pattern: bytes, data: bytes) -> list[int]:
    return [m.start() for m in re.finditer(pattern, data)]


def getSimilarityBetweenBuffers(buff1: bytes, buff2: bytes) -> float:
    return SequenceMatcher(a=buff1, b=buff2).quick_ratio()


def lookForPatternWithSimilarMatches(
        pattern: bytes,
        data: bytes,
        threshold: float = .5
) -> list:
    matches = []

    # FIXME
    # Need to make iterating better. Seems like matching atm is
    # enough, not exact, but is pretty damn close to how msftguy's
    # fuzzy_patcher works.

    for i in range(0, len(data), len(pattern)):
        buffer = getDataAtOffset(i, len(pattern), data)
        similarity = getSimilarityBetweenBuffers(pattern, buffer)

        if any((similarity == 0, similarity < threshold)):
            continue

        matches.append((round(similarity, 2), hex(i)))

    matches = sorted(matches, reverse=True)

    return matches
