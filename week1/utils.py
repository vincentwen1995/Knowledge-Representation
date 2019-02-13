#!/usr/bin/python


class Clause(object):
    '''Class for representing a clause.
    '''

    def __init__(self):
        pass


class Reader(object):
    '''Class for reading the input file.
    '''

    def __init__(self, file):
        self.file = file

    def read(self):
        with open(self.file, 'r') as input:
            for line in input:
                parsed = line.split()
                if parsed[0] == 'p':
                    var_cnts = int(parsed[2])
                    self.vars = [False for i in range(var_cnts)]
                elif parsed[0] == 'c':
                    continue
                else:
                    pass
