""" CLI for ml-stack """

import argparse
from mlstack.main import MLStack


def main():
    """ Main entrypoint for `ml-stack` CLI """
    parser = argparse.ArgumentParser(description="")
    subparsers = parser.add_subparsers(dest="command")

    setup = subparsers.add_parser("setup")
    args = parser.parse_args()

    if not args.command:
        parser.print_help()

    if args.command == "setup":
        MLStack().setup()
