#!/usr/bin/python
import random
import copy


class DP(object):
    '''Class for basic David-Putnams Solver
    '''
    
    def __init__(self, file):
        self.file = file
        self.split = 0
        
    def split_choice(self, clauses):
        if self.split == 1:
            return self.random_split(clauses)
        elif self.split == 2:
            raise NotImplementedError
        elif self.split == 3:
            raise NotImplementedError
        elif self.split == 4:
            raise NotImplementedError
        elif self.split == 5:
            raise NotImplementedError
    
    def solver(self, clauses):
        '''DP-Solver
        '''
        
        clauses = self.pure_literals(clauses)
        clauses = self.unit_clauses(clauses)
        if [] in clauses:
            return False
        if len(clauses) == 0:
            return self.vars
        split_var = self.split_choice(clauses)
        tmp = copy.deepcopy(clauses)
        assignment = self.solver(self.remove_clauses(split_var, clauses))
        if assignment == False:
            print('Backtracking...')
            clauses = copy.deepcopy(tmp)
            assignment = self.solver(self.remove_clauses(-split_var, clauses))
        return self.vars

    def random_split(self, clauses):
        '''Randomly choose a literal to split.
        '''
        
        clause = random.choice(clauses)
        split = random.choice(clause)
        return split

    def remove_clauses(self, variable, clauses):
        '''remove_clauses the clauses list with the given variable.
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
        '''Method for reading the clauses and do initial simplificaitons.
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
        '''Check and remove tautology.
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
        '''Collect the pure literals.
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
        '''Collect the variables in the unit clauses.
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
