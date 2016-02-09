#!/usr/bin/python
import mpd
from utils import dump

# use_unicode will enable the utf-8 mode for python2
# see http://pythonhosted.org/python-mpd2/topics/advanced.html#unicode-handling
client = mpd.MPDClient(use_unicode=True)
client.connect("10.0.0.10", 6600)

#info = client.lsinfo("/");

#dump(info)

#for entry in client.lsinfo("bfree"):
for entry in client.lsinfo("bfree/Unknown Album"):
    if 'directory' in entry:
        print entry['directory']
    else:
        print entry
#for key, value in client.status().items():
#    print("%s: %s" % (key, value))
