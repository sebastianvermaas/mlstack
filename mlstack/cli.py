""" CLI for ml-stack """

import argparse
from mlstack.main import MLStack


def main():
    """ Main entrypoint for `ml-stack` CLI """
    parser = argparse.ArgumentParser(description="")
    subparsers = parser.add_subparsers(dest="command")

    setup = subparsers.add_parser("setup")
    create = subparsers.add_parser("create")
    close = subparsers.add_parser("close")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()

    if args.command == "setup":
        MLStack().setup()

    if args.command == "create":
        MLStack().create()

    if args.command == "close":
        MLStack().close()
