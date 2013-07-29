#!/usr/bin/env python

'''Print a "word" of non-control and non-separator characters a line.'''

# http://stackoverflow.com/a/93029
# http://www.unicode.org/reports/tr44/#General_Category_Values

import sys
import re
from unicodedata import category as unicode_category

word_chars = u''.join(c for c in map(unichr, xrange(sys.maxunicode + 1))
                      if unicode_category(c)[0] not in 'CZ')

word_chars_pattern = re.compile(u'[%s]+' % re.escape(word_chars))

try:
    sys.stdout.writelines(match.group(0) + u'\n'
                          for line in fileinput.input()
                          for match in word_chars_pattern.finditer(line))
except IOError as e:
    if e.errno != 32:  # Ignore broken pipe
        raise e
