'''Protect help method from broken pipe by encasing it
in a try-except block.'''

try:
    help
except NameError:
    from pydoc import help

import sys

if len(sys.argv) > 1:
    module = sys.argv[1]
else:
    # module = sys.stdin.readline()
    sys.stderr.write('%s: argument required\n' % sys.argv[0])
    sys.exit(1)

try:
    help(module)
except IOError:# as e:
    ## shield broken pipe
    # if e.errno == 32:
    pass
