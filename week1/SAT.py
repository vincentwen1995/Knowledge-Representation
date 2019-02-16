#!/usr/bin/python
# # SAT solver script

import sys
from utils import Solver


def main(argv):
    sat_solver = Solver(argv[0])
    sat_solver.read()
    print('Overview:')
    print('\t No. of variables:', len(sat_solver.vars))
    print('\t No. of pure literals:', len(sat_solver.p_lits))
    print('\t No. of unit clauses:', len(sat_solver.unit_clauses))
    print('\t No. of clauses:', len(sat_solver.clauses))
    print('Variables:')
    print(sat_solver.vars)
    print('Pure literals:')
    print(sat_solver.p_lits)
    print('Unit clauses:')
    print(sat_solver.unit_clauses)
    print('Clauses:')
    print(sat_solver.clauses)


if __name__ == '__main__':
    main(sys.argv[1:])
