from os import mkdir
from os.path import isdir, expanduser, exists
from karos.core.utils import bcolors

def install():
	print "="*80, "\n", bcolors.BOLD, "\r", 'KarOS Installer', bcolors.ENDC, "\n" + "="*80
	d = expanduser("~/.karos")
	if not exists(d):
		if not isdir(d):
			print bcolors.OKGREEN, "Creating KarOS application directory at %(path)s" % {'path':d}, bcolors.ENDC
			mkdir(d)
		else:
			print bcolors.WARNING, "Warning: path %(path)s exists but is not a directory!" % {'path':d}, bcolors.ENDC
	else:
		print bcolors.WARNING, "Warning: path %(path)s/ already exists. Pre-existing configuration may be used." % {'path':d}, bcolors.ENDC

	print bcolors.OKGREEN, bcolors.BOLD, "\r", "KarOS Core Install Complete", bcolors.ENDC