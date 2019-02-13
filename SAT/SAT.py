#!/usr/bin/python
# # SAT solver script

import sys
from utils import Reader, Clause


def main(argv):
    reader = Reader(argv[1])


if __name__ == '__main__':
    main(sys.argv[1:])
