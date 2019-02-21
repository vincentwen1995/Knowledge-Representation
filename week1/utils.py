#!/usr/bin/python


class Solver(object):
    '''Class for reading the input file.
    '''

    def __init__(self, file):
        self.file = file
        self.clauses = []

    # def read(self):
    #     '''Method for reading the clauses and do initial simplificaitons.
    #     '''

    #     # Initialize variables.
    #     non_p_lits = []
    #     vars_tmp = set()
    #     immutable_vars = set()
    #     self.p_lits = []
    #     self.clauses = []

    #     # Start reading from the file.
    #     with open(self.file, 'r') as input_file:
    #         for line in input_file:
    #             parsed = line.split()

    #             # Check whether it is valid line or supplementary line.
    #             if parsed[0] == 'p' or parsed[0] == 'c':
    #                 continue
    #             else:
    #                 eff_parsed = parsed[:-1]

    #                 # Check for unit clauses.
    #                 if len(eff_parsed) == 1:
    #                     lit = eff_parsed[0]
    #                     int_lit = int(lit)
    #                     abs_lit = str(abs(int_lit))
    #                     neg_lit = str(-int_lit)

    #                     # Check if problem is solvable.
    #                     if neg_lit in immutable_vars:
    #                         self.output_result('no')

    #                     # Collect immutable variables.
    #                     immutable_vars.add(lit)

    #                     # Collect variable.
    #                     vars_tmp.add(abs_lit)

    #                     # Check for pure literals.
    #                     if neg_lit not in self.p_lits:
    #                         if lit not in self.p_lits and abs_lit not in non_p_lits:
    #                             self.p_lits.append(lit)
    #                     else:
    #                         self.p_lits.remove(neg_lit)
    #                         non_p_lits.append(abs_lit)
    #                 else:
    #                     self.clauses.append(list())
    #                     clause = self.clauses[-1]
    #                     tautology = False
    #                     for lit in eff_parsed:
    #                         int_lit = int(lit)
    #                         clause.append(lit)

    #                         # Collect variable.
    #                         abs_lit = str(abs(int_lit))
    #                         vars_tmp.add(abs_lit)

    #                         # Check for tautology.
    #                         neg_lit = str(-int_lit)
    #                         if neg_lit in clause:
    #                             tautology = True

    #                         # Check for pure literals.
    #                         if neg_lit not in self.p_lits:
    #                             if lit not in self.p_lits and abs_lit not in non_p_lits:
    #                                 self.p_lits.append(lit)
    #                         else:
    #                             self.p_lits.remove(neg_lit)
    #                             non_p_lits.append(abs_lit)

    #                     # Remove clauses with tautology.
    #                     if tautology:
    #                         self.clauses.pop()

    #     # Initialize all collected variables, e.g. {'115': [0, False] ...} - where [truth_val, mutability]
    #     self.vars = dict.fromkeys(vars_tmp, [0, True])
    #     self.imvars = immutable_vars
    #     for var in immutable_vars:
    #         int_var = int(var)
    #         var_ind = str(abs(int_var))
    #         if int_var < 0:
    #             self.vars[var_ind] = [-1, False]
    #         else:
    #             self.vars[var_ind] = [1, False]
    #     for var in self.p_lits:
    #         int_var = int(var)
    #         var_ind = str(abs(int_var))
    #         if int_var < 0:
    #             self.vars[var_ind] = [-1, False]
    #         else:
    #             self.vars[var_ind] = [1, False]

    def read(self):
        '''Method for reading the clauses and do initial simplificaitons.
        '''

        # Initialize variables.
        vars_tmp = set()
        clauses = set()
        # Start reading from the file.
        with open(self.file, 'r') as input_file:
            for line in input_file:
                parsed = line.split()

                # Check whether it is valid line or supplementary line.
                if parsed[0] == 'p' or parsed[0] == 'c':
                    continue
                else:
                    eff_parsed = parsed[:-1]
                    clause = set()
                    for lit in eff_parsed:
                        lit = int(lit)
                        clause.add(lit)

                        # Collect variable.
                        abs_lit = abs(lit)
                        vars_tmp.add(abs_lit)
                    clauses.add(list(clause))

        # Initialize all collected variables, e.g. {'115': [0, False] ...} - where [truth_val, mutability]
        self.vars = dict.fromkeys(vars_tmp, False)
        self.clauses = list(clauses)

    def tautology(self):
        '''Check and remove tautology.
        '''

        for clause in self.clauses:
            if len(clause) == 1:
                continue
            else:
                for lit in clause:
                    if -lit in clause:
                        self.clauses.remove(clause)
                        break

    def pure_literals(self):
        '''Collect the pure literals.
        '''

        self.p_lits = []
        non_p_lits = []
        for clause in self.clauses:
            for lit in clause:
                neg_lit = -lit
                abs_lit = abs(lit)
                if neg_lit not in self.p_lits:
                    if lit not in self.p_lits and abs_lit not in non_p_lits:
                        self.p_lits.append(lit)
                else:
                    self.p_lits.remove(neg_lit)
                    non_p_lits.append(abs_lit)

    def unit_clauses(self):
        '''Collect the variables in the unit clauses.
        '''

        self.unit_var = set()
        for clause in self.clauses:
            if len(clause) == 1:
                self.unit_var.add(clause[0])

    def output_result(self, flag='yes'):
        '''Method for printing the final results.

        Keyword Arguments:
            flag {str} -- flag to indicate whether there is a solution to the problem (default: {'yes'})
        '''

        if flag == 'yes':
            cnt = len(self.vars)
            print('p cnf {} {}'.format(cnt, cnt))
            for k in sorted(self.vars.iterkeys()):
                if self.vars[k]:
                    print(k + ' 0')
                else:
                    print('-' + k + ' 0')
        else:
            print('The problem is unsolvable.')
