
from argparse import ArgumentParser

from .diff import diffToJSONFile, readDifferencesFromJSONFile
from .file import readDataFromPath
from .find import findPatternsFromDifferences


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument('-orig', nargs=1)
    parser.add_argument('-new', nargs=1)
    parser.add_argument('-json', nargs=1)

    parser.add_argument('-diff', action='store_true')
    parser.add_argument('-patch', action='store_true')
    parser.add_argument('-find', action='store_true')

    args = parser.parse_args()

    if not any((args.diff, args.patch, args.find, args.orig, args.json)):
        return parser.print_help()

    origData = readDataFromPath(args.orig[0])

    if all((args.diff, args.new, not args.patch)):
        newData = readDataFromPath(args.new[0])
        diffToJSONFile(origData, newData, args.json[0])

    elif all((args.patch, args.new, not args.diff)):
        # differences = readDifferencesFromJSONFile(args.json[0])
        # newData = applyPatchesFromDifferences(differences, origData)
        # writeDataToPath(args.new[0], newData)

        pass

    elif all((args.find, not args.diff, not args.patch)):
        differences = readDifferencesFromJSONFile(args.json[0])
        findPatternsFromDifferences(differences, origData)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
