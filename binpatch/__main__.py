
from argparse import ArgumentParser

from .diff import diffToJSONFile
from .file import readDataFromPath


def main():
    parser = ArgumentParser()

    parser.add_argument('-orig', nargs=1)
    parser.add_argument('-patched', nargs=1)
    parser.add_argument('-json', nargs=1)

    args = parser.parse_args()

    if all((args.orig, args.patched, args.json)):
        orig_data = readDataFromPath(args.orig[0])
        patched_data = readDataFromPath(args.patched[0])
        diffToJSONFile(orig_data, patched_data, args.json[0])

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
