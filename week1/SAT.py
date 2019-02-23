#!/usr/bin/python
# # SAT solver script

import sys
from utils import DP
from printSudoku import print_sudoku
from printSudoku import check_sudoku


def main(argv):
    if argv[0] == '-S1':
        sat_solver = DP(argv[1])
        sat_solver.split = 1
    elif argv[0] == '-S2':
        sat_solver = DP(argv[1])
        sat_solver.split = 2
    elif argv[0] == '-S3':
        sat_solver = DP(argv[1])
        sat_solver.split = 3
    elif argv[0] == '-S4':
        sat_solver = DP(argv[1])
        sat_solver.split = 4
    elif argv[0] == '-S5':
        sat_solver = DP(argv[1])
        sat_solver.split = 5
    else:
        print('Incorrect input: your input command should be strictly of the following format:')
        print("for Linux: 'sh SAT.sh -Sn inputfile' (where n = 1 ~ 5)")
        print("for Windows: 'SAT.bat -Sn inputfile' (where n = 1 ~ 5)")
        exit()
    clauses = sat_solver.read()
    clauses = sat_solver.tautology(clauses)
    var = sat_solver.solver(clauses)
    if var is False:
        print('Oops, the problem is not solvable...')
        exit()
    truth = [literal for literal, value in var.items() if value is True]
    print('The number of TRUE variable is:', len(truth))
    print_sudoku(truth)
    check_sudoku(truth)


if __name__ == '__main__':
    main(sys.argv[1:])
