#!/usr/bin/env python


__all__ = ['solve']


from numbers import Number


#_exprs = {
#    'abxy': 'a/b = x/y',
#    'ab'  : 'x/y',
#    'a'   : 'bx/y',
#    'b'   : 'ay/x',
#    'xy'  : 'a/b',
#    'x'   : 'ay/b',
#    'y'   : 'bx/a',
#}


VARS = frozenset('abxy')

# KEEP THESE SEQUENCES IN THE GIVEN ORDER
# it's how the universal solver receives the arguments
# see the commented-out dict above
VAR_ORDERS = ('bxy', 'ayx', 'ayb', 'bxa')

ORDERING = dict((frozenset(v), v) for v in VAR_ORDERS)


def solve(**kw):
    '''For the equation
    
    >>> a/b = x/y
    
    give 3 of the arguments as keywords, e.g. solve(a=a, b=b, x=x),
    and solve for the missing variable.

    '''
    #if len(kw) != 3:
    #    raise TypeError('Expected 3 named arguments, got %d' % len(kw))
    # Filter for only valid var names
    d = dict((k, v) for (k, v) in kw.iteritems()
             if k in VARS and issubclass(type(v), Number))
    if len(d) != 3:
        raise TypeError('Expected 3 named arguments, got %d' % len(kw))
    # Extract the ordered vars into a generic operation
    var_order = ORDERING[frozenset(d.iterkeys())]
    j, k, l = tuple(kw[v] for v in var_order)
    return j * k / l


if __name__ == '__main__':
    import sys
    kw = {}
    for arg in sys.argv[1:]:
        k, v = arg.split('=', 1)
        kw[k] = v
    print solve(**kw)
