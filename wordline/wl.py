#!/usr/bin/env python

'''Print a word a line.'''

from sys import stdout
from re import finditer
import fileinput

try:
    stdout.writelines(match.group(0) + '\n'
                      for line in fileinput.input()
                      for match in finditer(r'\w+', line))
except IOError as e:
    if e.errno != 32:  # Ignore broken pipe
        raise e
