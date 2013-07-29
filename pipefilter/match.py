#!/usr/bin/env python

import sys
import os
import re

if len(sys.argv) < 2:
    sys.stderr.write("usage: %s PATTERN [STRINGS...]\n" % sys.argv[0])
    sys.exit(2)

pattern = re.compile(sys.argv[1])

n = 0

def filter_stream(stream):
    global n
    for item in stream:
        if pattern.search(item):
            n += 1
            sys.stdout.write(item + ('\n' if item[-1] != '\n' else ''))

try:
    filter_stream(sys.argv[2:])

    if not sys.stdin.isatty():
        filter_stream(sys.stdin)

except IOError as e:
    if e.errno != 32:  # Ignore broken pipe
        sys.stderr.write("%s: %s\n" % (sys.argv[0], e.strerror))
        sys.exit(e.errno)

finally:
    # Without these, catching a broken pipe leads to strange errors
    sys.stdout.close()
    sys.stderr.close()

sys.exit(0 if n else 1)
