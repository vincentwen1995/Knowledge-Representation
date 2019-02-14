#!/usr/bin/python
# # SAT solver script

import sys
from utils import Reader


def main(argv):
    reader = Reader(argv[0])
    reader.read()
    print('Overview:')
    print('\t No. of variables:', len(reader.vars))
    print('\t No. of pure literals:', len(reader.p_lits))
    print('\t No. of unit clauses:', len(reader.unit_clauses))
    print('\t No. of clauses:', len(reader.clauses))
    print('Variables:')
    print(reader.vars)
    print('Pure literals:')
    print(reader.p_lits)
    print('Unit clauses:')
    print(reader.unit_clauses)
    print('Clauses:')
    print(reader.clauses)


if __name__ == '__main__':
    main(sys.argv[1:])
