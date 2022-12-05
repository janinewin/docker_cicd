import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--number", required=True, type=int)
    return parser.parse_args()
