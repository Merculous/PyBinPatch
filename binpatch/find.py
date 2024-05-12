
import re


def lookForPatternWithExactMatches(pattern: bytes, data: bytes) -> list[int]:
    return [m.start() for m in re.finditer(pattern, data)]
