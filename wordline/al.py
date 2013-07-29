#!/usr/bin/env python

'''Print an argument a line.'''

from sys import argv, exit, stdout

try:
    stdout.writelines(arg + '\n' for arg in argv[1:])
except IOError as e:
    if e.errno != 32:  # Ignore broken pipe
        raise e
