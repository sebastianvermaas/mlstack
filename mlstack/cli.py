""" CLI for ml-stack """

import argparse
from mlstack.run import MLStack


def main():
    parser = argparse.ArgumentParser(description="")
    subparsers = parser.add_subparsers(dest="command")
    subparser_build = subparsers.add_parser("build")
    subparser_build.add_argument("-c", "--config", type=str, default=None)
    subparser_build.add_argument("-t", "--tags", default=None)

    subparser_build = subparsers.add_parser("apply")

    args = parser.parse_args()

    if args.command == "build":
        MLStack(args.config).dockerbuild(args.tags)
