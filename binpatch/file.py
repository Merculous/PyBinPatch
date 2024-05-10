
def readDataFromPath(path: str) -> bytes:
    with open(path, 'rb') as f:
        return f.read()
