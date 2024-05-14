
def getDataAtOffset(offset: int, buffSize: int, data: bytes) -> bytes:
    return data[offset:offset+buffSize]
