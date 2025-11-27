
from argparse import ArgumentParser
from pathlib import Path
from time import perf_counter

from .diff import diffToJSONFile, readDifferencesJSONFile
from .io import readBytesFromPath, writeBytesToPath
from .patch import patchFromDifferences


def diffFiles(src1Path: Path, src2Path: Path, jsonPath: Path) -> None:
    aData = readBytesFromPath(src1Path)
    bData = readBytesFromPath(src2Path)
    diffToJSONFile(aData, bData, jsonPath)


def patchFile(src1Path: Path, src2Path: Path, jsonPath: Path) -> None:
    aData = bytearray(readBytesFromPath(src1Path))
    differences = readDifferencesJSONFile(jsonPath)
    patched = patchFromDifferences(aData, differences)
    writeBytesToPath(src2Path, patched)


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument('-a', type=Path)
    parser.add_argument('-b', type=Path)
    parser.add_argument('-json', type=Path)

    parser.add_argument('--diff', action='store_true')
    parser.add_argument('--patch', action='store_true')

    args = parser.parse_args()
    startTime = perf_counter()

    if args.diff:
        diffFiles(args.a, args.b, args.json)

    elif args.patch:
        patchFile(args.a, args.b, args.json)

    else:
        return parser.print_help()

    endTime = perf_counter() - startTime
    print(f'Ran in {endTime:.4f} seconds!')


if __name__ == '__main__':
    main()
