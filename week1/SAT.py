#!/usr/bin/python
# # SAT solver script

import sys
from utils import DP
from printSudoku import print_sudoku
from printSudoku import check_sudoku


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
    truth = [literal for literal, value in var.items() if value == True]
    print(len(truth))
    print_sudoku(truth)
    check_sudoku(truth)


if __name__ == '__main__':
    main(sys.argv[1:])
