""" CLI for ml-stack """

import argparse
from mlstack.run import MLStack


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-c", "--config", type=str, default=None)
    args = parser.parse_args()
