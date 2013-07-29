#!/usr/bin/env python


import sys
import fileinput


ACTIONS = ('get', 'set', 'delete', 'replace')


class AssocError(RuntimeError):

    def __init__(self, message=None):
        RuntimeError.__init__(self, message)

    def write(self, outfile=sys.stderr):
        outfile.write(self.message + '\n')

    def exit(self):
        sys.exit(self.__class__.EXIT_STATUS)


class Usage(AssocError):
    """shell usage message"""

    USAGE = ("usage: assoc get|set|delete|replace "
             "key [value] {key value}...")

    EXIT_STATUS = 2

    def __init__(self, message=None):
        if message is not None:
            message = str(message) + '\n' + Usage.USAGE
        else:
            message = Usage.USAGE
        AssocError.__init__(self, message)

    def exit(self, outfile=sys.stderr):
        self.write(outfile)
        super(self.__class__, self).exit()


class KeyNotFound(AssocError):
    """key not found for get, delete, replace"""
    EXIT_STATUS = 1


def tryrun(f, *args, **kwds):
    try:
        f(*args, **kwds)
    except (Usage, KeyNotFound) as e:
        e.exit()

    # http://bugs.python.org/issue11380
    # http://stackoverflow.com/a/8690674/637397
    #
    # BUGFIX: Prevent a broken pipe from trashing sys.stderr
    try:
        sys.stdout.close()
    except:
        pass
    try:
        sys.stderr.close()
    except:
        pass


def getaction(arg):
    for action in ACTIONS:
        if arg == action[:len(arg)]:
            return action
    else:
        raise Usage("not an action: " + arg)


def getstream(argv, start, infile=sys.stdin):
    nofilenames = True

    if len(argv) > start:
        if argv[start] == "--":  # end-of-options arg
            start += 1
        elif argv[start] == "-f":  # file names given as args
            nofilenames = False
            start += 1

    if nofilenames:
        if len(argv) > start:
            return argv[start:]
        else:
            return (line[:-1] for line in infile)  # chomp EOL
    else:
        return fileinput.input(argv[start:])


def pairs(it):
    """Group stream into 2-tuples to pass to dict.

    Ignore a trailing key.

    """
    isfirst, firstval = True, None
    for v in it:
        if isfirst:
            isfirst, firstval = False, v
        else:
            isfirst = True
            yield firstval, v


def output(assoc, outfile=sys.stdout):
    """print dict assoc as an assoc list"""
    for k,v in assoc.iteritems():
        outfile.write("%s\n%s\n" % (k, v))


def main(argv=sys.argv, infile=sys.stdin, outfile=sys.stdout):
    if len(argv) <= 2:
        usage()

    action = getaction(argv[1])
    key = argv[2]

    if action == "set" or action == "replace":
        if len(argv) <= 3:
            raise Usage("set and replace need key and value")
        val = argv[3]
        start = 4
    else:
        start = 3

    stream = getstream(argv, start, infile)
    assoc = dict(pairs(stream))

    keyfound = True

    if action == "get":
        val = assoc.get(key, None)
        if val is not None:
            outfile.write(val + "\n")
            return
        else:
            raise KeyNotFound(key)
    elif action == "set":
        assoc[key] = val
    elif action == "delete":
        if key in assoc:
            del assoc[key]
        else:
            keyfound = False
    else:  # action == "replace"
        if key in assoc:
            assoc[key] = val
        else:
            keyfound = False

    output(assoc, outfile)

    if not keyfound:
        raise KeyNotFound(key)


if __name__ == '__main__':
    tryrun(main)
