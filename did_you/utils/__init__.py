import sys

def cmdline_args(decoratee):
    arguments = sys.argv[1:]
    if len(arguments) == 0:
        decoratee(None)
    else:
        decoratee(arguments)
