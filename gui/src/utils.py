import pprint

# Console color termcap codes
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def dump(arg):
    print "="*80, "\n", bcolors.BOLD, arg, bcolors.ENDC, "\n" + "="*80, bcolors.WARNING
    col_width = max(len(row) for row in dir(arg)) + 3
    for d in dir(arg):
        try:
            print d.ljust(col_width) + " : " + str(getattr(arg,d))
        except AttributeError:
            print "AttributeError: {} -- {}".format(d, d  )

    try:
        pprint.pprint(vars(arg))
    except TypeError:
        pass
    print bcolors.ENDC    