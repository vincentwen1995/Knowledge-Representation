#!/usr/bin/python
# # SAT solver script

import sys
from utils import DP


def main(argv):
    if argv[0] == '-S1':
        sat_solver = DP(argv[1]) 
    elif argv[0] == '-S2':
        pass
    elif argv[0] == '-S3':
        pass
    else:
        print('WARNING: your input command should be strictly of the following format:')
        print('sh SAT.sh -Sn inputfile (where n = 1, 2 or 3)')
        exit()
    clauses = sat_solver.read()
    clauses = sat_solver.tautology(clauses)
    var = sat_solver.solver(clauses)
    print(var)


if __name__ == '__main__':
    main(sys.argv[1:])
