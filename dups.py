#!/usr/bin/env python

import sys
import collections

try:
    n = int(sys.argv[1])
except:
    n = 2

if n < 2:
    n = 2

cache = collections.Counter()

try:
    for line in sys.stdin:
        cache[line] += 1
        if cache[line] == n:
            sys.stdout.write(line)
except IOError as e:
    if e.errno != 32:  # Ignore broken pipe
        sys.stderr.write("%s: %s\n" % (sys.argv[0], e.strerror))
        sys.exit(e.errno)
finally:
    # Necessary to avoid a bug which causes strange errors
    # when catching a broken pipe.
    sys.stdout.close()
    sys.stderr.close()
