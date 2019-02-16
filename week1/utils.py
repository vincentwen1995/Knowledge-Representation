#!/usr/bin/python


class Reader(object):
    '''Class for reading the input file.
    '''

    def __init__(self, file):
        self.file = file

    def read(self):
        # Initialize variables.
        non_p_lits = []
        vars_tmp = set()
        self.p_lits = []
        self.clauses = []
        self.unit_clauses = []
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
                        clause.append(lit)
                        # Collect unit clauses.
                        self.unit_clauses.append(clause)
                        # Collect variable.
                        int_lit = int(lit)
                        abs_lit = str(abs(int_lit))
                        vars_tmp.add(abs_lit)
                        # Check for pure literals.
                        neg_lit = str(-int_lit)
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
        # Initialize all collected variables.
        self.vars = dict.fromkeys(vars_tmp, False)
