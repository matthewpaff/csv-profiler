import argparse
import json
import sys

from .core import profile
from .fixture_check import check


def main(argv=None):
    parser = argparse.ArgumentParser(description="Profile a small UTF-8 CSV file as JSON.")
    parser.add_argument("path", nargs="?", default="-", help="File or - for stdin")
    parser.add_argument("--delimiter", default=",")
    parser.add_argument("--check-fixtures", metavar="JSONL")
    args = parser.parse_args(argv)
    try:
        if args.check_fixtures:
            if args.path != "-" or args.delimiter != ",":
                parser.error("Use --check-fixtures alone")
            print("Verified {} synthetic fixtures.".format(check(args.check_fixtures, profile)))
        else:
            if args.path == "-":
                text = sys.stdin.read()
            else:
                with open(args.path, encoding="utf-8-sig", newline="") as handle:
                    text = handle.read()
            print(json.dumps(profile(text, args.delimiter), indent=2, ensure_ascii=True))
        return 0
    except ValueError as error:
        print("error: " + str(error), file=sys.stderr)
        return 2
    except OSError as error:
        print("error: " + str(error), file=sys.stderr)
        return 1
