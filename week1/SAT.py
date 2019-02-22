#!/usr/bin/python
# # SAT solver script

import sys
from utils import Solver


def main(argv):
    sat_solver = Solver(argv[0])
    clauses = sat_solver.read()
    clauses = sat_solver.tautology(clauses)
    var = sat_solver.solver(clauses)
    print(var)


if __name__ == '__main__':
    main(sys.argv[1:])
