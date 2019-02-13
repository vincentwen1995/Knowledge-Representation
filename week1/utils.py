#!/usr/bin/python


class Reader(object):
    '''Class for reading the input file.
    '''

    def __init__(self, file):
        self.file = file

    def read(self):
        non_p_lits = []
        self.p_lits = []
        self.clauses = []
        self.unit_clauses = []
        with open(self.file, 'r') as input_file:
            for line in input_file:
                parsed = line.split()
                if parsed[0] == 'p':
                    var_cnts = int(parsed[2])
                    self.vars = [False for i in range(var_cnts)]
                elif parsed[0] == 'c':
                    continue
                else:
                    eff_parsed = parsed[:-1]
                    # Check for unit clauses.
                    if len(eff_parsed) == 1:
                        self.unit_clauses.extend(eff_parsed)
                        continue

                    clause = []
                    for lit in eff_parsed:
                        # Check for tautology.
                        neg_lit = str(-int(lit))
                        if neg_lit in clause:
                            clause.remove(neg_lit)
                            continue
                        clause.append(lit)

                        # Check for pure literals.
                        if neg_lit not in self.p_lits:
                            if lit not in non_p_lits:
                                self.p_lits.append(lit)
                        else:
                            self.p_lits.remove(neg_lit)
                            non_p_lits.append(lit)
                            non_p_lits.append(neg_lit)

                    self.clauses.append(clause)
