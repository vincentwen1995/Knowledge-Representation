#!/usr/bin/python


class Solver(object):
    '''Class for reading the input file.
    '''

    def __init__(self, file):
        self.file = file

    def read(self):
        '''Method for reading the clauses and do initial simplificaitons.
        '''

        # Initialize variables.
        non_p_lits = []
        vars_tmp = set()
        immutable_vars = []
        self.p_lits = []
        self.clauses = []
        # Start reading from the file.
        with open(self.file, 'r') as input_file:
            for line in input_file:
                parsed = line.split()
                # Check whether it is valid line or supplementary line.
                if parsed[0] == 'p' or parsed[0] == 'c':
                    continue
                else:
                    self.clauses.append(list())
                    clause = self.clauses[-1]
                    tautology = False
                    eff_parsed = parsed[:-1]
                    # Check for unit clauses.
                    if len(eff_parsed) == 1:
                        lit = eff_parsed[0]
                        int_lit = int(lit)
                        abs_lit = str(abs(int_lit))
                        neg_lit = str(-int_lit)
                        clause.append(lit)
                        # Check if problem is solvable.
                        if neg_lit in immutable_vars:
                            self.output_result('no')
                        # Collect immutable variables.
                        immutable_vars.extend(clause)
                        # Collect variable.
                        vars_tmp.add(abs_lit)
                        # Check for pure literals.
                        if neg_lit not in self.p_lits:
                            if lit not in self.p_lits and abs_lit not in non_p_lits:
                                self.p_lits.append(lit)
                        else:
                            self.p_lits.remove(neg_lit)
                            non_p_lits.append(abs_lit)
                    else:
                        for lit in eff_parsed:
                            int_lit = int(lit)
                            clause.append(lit)
                            # Collect variable.
                            abs_lit = str(abs(int_lit))
                            vars_tmp.add(abs_lit)
                            # Check for tautology.
                            neg_lit = str(-int_lit)
                            if neg_lit in clause:
                                tautology = True
                            # Check for pure literals.
                            if neg_lit not in self.p_lits:
                                if lit not in self.p_lits and abs_lit not in non_p_lits:
                                    self.p_lits.append(lit)
                            else:
                                self.p_lits.remove(neg_lit)
                                non_p_lits.append(abs_lit)
                        # Remove clauses with tautology.
                        if tautology:
                            self.clauses.pop()
        # Initialize all collected variables, e.g. {'115': [0, False] ...} - where [truth_val, mutability]
        self.vars = dict.fromkeys(vars_tmp, [0, True])
        for var in immutable_vars:
            int_var = int(var)
            var_ind = str(abs(int_var))

            if int_var < 0:
                self.vars[var_ind] = [-1, False]
            else:
                self.vars[var_ind] = [1, False]

    def evaluate_clause(self, clause):
        '''Evaluate the truth of a clause.

        Arguments:
            clause {list} -- list of literals

        Returns:
            bool/str -- truth of the clause (or 'unk')
        '''

        res = False
        unks = 0
        for lit in clause:
            int_lit = int(lit)
            if int_lit < 0:
                val = -self.vars[str(abs(int_lit))][0]
            else:
                val = self.vars[str(abs(int_lit))][0]
            if val > 0:
                res = True
                break
            elif val == 0:
                unks += 1
        if unks == len(clause):
            res = 'unk'
        return res

    def evalute(self, clauses):
        '''Evaluate the problem.

        Arguments:
            clauses {list} -- list of clauses

        Returns:
            bool/str -- truth of the problem (or 'unk')
        '''

        res = []
        for clause in clauses:
            res_tmp = self.evaluate_clause(clause)
            if res_tmp == 'unk':
                return 'unk'
            res.append(res_tmp)
        return all(res)

    def output_result(self, flag='yes'):
        '''Method for printing the final results.

        Keyword Arguments:
            flag {str} -- flag to indicate whether there is a solution to the problem (default: {'yes'})
        '''

        if flag == 'yes':
            cnt = len(self.vars)
            print('p cnf {} {}'.format(cnt, cnt))
            for k in sorted(self.vars.iterkeys()):
                if self.vars[k][0] < 0:
                    print('-' + k + ' 0')
                else:
                    print(k + ' 0')
        else:
            print('The problem is unsolvable.')
