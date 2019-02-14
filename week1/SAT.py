#!/usr/bin/python
# # SAT solver script

import sys
from utils import Reader


def main(argv):
    reader = Reader(argv[0])
    reader.read()
    print('Pure literals:')
    print(reader.p_lits)
    print('Unit clauses:')
    print(reader.unit_clauses)
    print('Variables:')
    print(reader.vars)
    print('Clauses:')
    print(reader.clauses)


if __name__ == '__main__':
    main(sys.argv[1:])
