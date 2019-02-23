#!/usr/bin/python
# # SAT solver script

import sys
from utils import DP
from printSudoku import print_sudoku
from printSudoku import check_sudoku


def main(argv):
    if argv[0] == '-S1':
        print('The strategy you choose is: Random Split.')
        sat_solver = DP(argv[1])
        sat_solver.split = 1
    elif argv[0] == '-S2':
        print('The strategy you choose is: (Deterministic) Jeroslow-Wang Split.')
        sat_solver = DP(argv[1])
        sat_solver.split = 2
    elif argv[0] == '-S3':
        print('The strategy you choose is: Probabilistic Jeroslow-Wang Split.')
        sat_solver = DP(argv[1])
        sat_solver.split = 3
    elif argv[0] == '-S4':
        print('The strategy you choose is: (Deterministic) DLIS.')
        sat_solver = DP(argv[1])
        sat_solver.split = 4
    elif argv[0] == '-S5':
        print('The strategy you choose is: Probabilistic DLIS.')
        sat_solver = DP(argv[1])
        sat_solver.split = 5
    else:
        print('Incorrect input: your input command should be strictly of the following format:')
        print('--------------------')
        print("for Linux: 'sh SAT.sh -Sn inputfile'")
        print("for Windows: 'SAT.bat -Sn inputfile'")
        print('--------------------')
        print("Note: n can be 1 ~ 5, which corresponds to 5 different splitting strategies.")
        exit()
    print('--------------------')
    print('Processing...')
    print('--------------------')
    clauses = sat_solver.read()
    clauses = sat_solver.tautology(clauses)
    var = sat_solver.solver(clauses)
    print('Done!')
    print('--------------------')
    if var is False:
        print('Oops, the problem is not solvable...')
        exit()
    truth = [literal for literal, value in var.items() if value is True]
    print('The number of splitting + backtracking is:', sat_solver.count)
    # print('The number of TRUE variable is:', len(truth))
    print_sudoku(truth)
    check_sudoku(truth)


if __name__ == '__main__':
    main(sys.argv[1:])
