#!/usr/bin/python
import random
import copy
from collections import defaultdict


class DP(object):
    '''Class for David-Putnam solver.
    '''

    def __init__(self, file):
        self.file = file
        self.split = 0
        self.n = 0
        self.modified = 0

    def split_choice(self, clauses):
        '''Select heuristics to split.

        Arguments:
            clauses {list} -- list of clauses

        Returns:
            int -- variable to split
        '''

        if self.split == 1:
            return self.random_split(clauses)
        elif self.split == 2:
            return self.JW_det_split(clauses)
        elif self.split == 3:
            return self.JW_prob_split(clauses)
        elif self.split == 4:
            raise NotImplementedError
        elif self.split == 5:
            raise NotImplementedError

    def solver(self, clauses):
        '''Main method of solver.

        Arguments:
            clauses {list} -- list of clauses

        Returns:
            dict -- dictionary of variables with assigned values
        '''

        self.n = self.n + 1
        print('start n:', self.n)
        print('start:', clauses)
        clauses = self.pure_literals(clauses)
        print('after pure:', clauses)
        clauses = self.unit_clauses(clauses)
        print('after unit:', clauses)
        if [] in clauses:
            return False
        if len(clauses) == 0:
            print('success!', self.vars)
            return self.vars
        split_var = self.split_choice(clauses)
        print(split_var, clauses)
        if self.modified == 0:
            tmp = copy.deepcopy(clauses)
            self.modified = 1
        print('tmp:', tmp)
        assignment = self.solver(self.remove_clauses(split_var, clauses))
        print('after n:', self.n)
        print('after:', clauses, tmp)
        if assignment == False:
            clauses = tmp
            self.modified = 0
            print('new try:', clauses)
            assignment = self.solver(self.remove_clauses(-split_var, clauses))
        return self.vars

    def random_split(self, clauses):
        '''Random splitting heuristic.

        Arguments:
            clauses {list} -- list of clauses

        Returns:
            int -- variable to split
        '''

        clause = random.choice(clauses)
        split = random.choice(clause)
        return split

    def remove_clauses(self, variable, clauses):
        '''Update the list of clauses with the given variable assigned.

        Arguments:
            variable {int} -- variable with assgined value
            clauses {list} -- list of clauses

        Returns:
            list -- updated list of clauses
        '''

        new_clauses = []
        if variable >= 0:
            self.vars[variable] = True
        else:
            self.vars[abs(variable)] = False
        for clause in clauses:
            if variable in clause:
                continue
            else:
                if -variable in clause:
                    clause.remove(-variable)
                new_clauses.append(clause)
        return new_clauses

    def read(self):
        '''Method for reading the clauses from the input file.

        Returns:
            list -- list of clauses
        '''

        # Initialize clauses list.
        clauses = []

        # Initialize variables.
        vars_tmp = set()

        # Start reading from the file.
        with open(self.file, 'r') as input_file:
            for line in input_file:
                parsed = line.split()

                # Check whether it is valid line or supplementary line.
                if not parsed or parsed[0] == 'p' or parsed[0] == 'c':
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
                    clauses.append(list(clause))

        # Initialize all collected variables, e.g. {'115': [0, False] ...} - where [truth_val, mutability]
        self.vars = dict.fromkeys(vars_tmp, False)
        return clauses

    def tautology(self, clauses):
        '''Check and remove tautology from the list of clauses.

        Returns:
            list -- list of clauses
        '''

        new_clauses = []
        check = 1
        for clause in clauses:
            for lit in clause:
                if -lit in clause:
                    check = 0
                    break
            if check == 1:
                new_clauses.append(clause)
            else:
                check = 1
        return new_clauses

    def pure_literals(self, clauses):
        '''Collect and remove the pure literals from the list of clauses.

        Returns:
            list -- list of clauses
        '''

        p_lits = set()
        non_p_lits = set()
        for clause in clauses:
            for lit in clause:
                neg_lit = -lit
                abs_lit = abs(lit)
                if neg_lit not in p_lits:
                    if abs_lit not in non_p_lits:
                        p_lits.add(lit)
                else:
                    p_lits.remove(neg_lit)
                    non_p_lits.add(abs_lit)
        for lit in p_lits:
            clauses = self.remove_clauses(lit, clauses)
        return clauses

    def unit_clauses(self, clauses):
        '''Collect and remove unit clauses from the list of clauses.

        Returns:
            list -- list of clauses
        '''

        unit_var = set()
        for clause in clauses:
            if len(clause) == 1:
                unit_var.add(clause[0])
        while len(unit_var) > 0:
            for unit in unit_var:
                clauses = self.remove_clauses(unit, clauses)
            unit_var = set()
            clauses = self.unit_clauses(clauses)
        return clauses

    def JW_det_split(self, clauses):
        '''Use deterministic Jeroslow-Wang heuristics to split variable.

        Arguments:
            clauses {list} -- list of clauses

        Returns:
            int -- selected variable to split
        '''

        J = defaultdict(int)
        for clause in clauses:
            clause_len = len(clause)
            for lit in clause:
                J[lit] += 2 ** (-clause_len)

        max_pair = [-1, 0]
        for k in J.keys():
            sum_J = J[k] + J[-k]
            if sum_J > max_pair[1] and max_pair[0] != -k:
                max_pair = [k, sum_J]

        split = abs(max_pair[0])
        if J[split] >= J[-split]:
            return split
        else:
            return -split

    def JW_prob_split(self, clauses):
        '''Use probabilistic Jeroslow-Wang heuristics to split variable.

        Arguments:
            clauses {list} -- list of clauses

        Returns:
            int -- selected variable to split
        '''

        J = defaultdict(int)
        for clause in clauses:
            clause_len = len(clause)
            for lit in clause:
                J[lit] += 2 ** (-clause_len)

        choices = []
        vals = []
        for k, v in J.items():
            lit = abs(k)
            if lit not in choices:
                choices.append(lit)
                vals.append(J[k] + J[-k])

        split = random.choices(choices, weights=vals, k=1)
        split = split[0]

        split = random.choices([split, -split], weights=[J[split], J[-split]], k=1)
        split = split[0]
        return split
