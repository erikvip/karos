#!/usr/bin/python
import mpd
import sys
#from utils import dump

# From bash: python ./mpd-test.py | cut -d' ' -f2- | sed "s/u'/'/g" | tr "'" '"' | jq .
# use_unicode will enable the utf-8 mode for python2
# see http://pythonhosted.org/python-mpd2/topics/advanced.html#unicode-handling
client = mpd.MPDClient(use_unicode=True)
client.connect("10.0.0.211", 6600)

#info = client.lsinfo("/");

#dump(info)



#for entry in client.lsinfo("bfree"):
#for entry in client.lsinfo("ACDC/Ballbreaker"):
#    if 'directory' in entry:
#        print entry['directory']
#    else:
#        print entry
#for key, value in client.status().items():
#    print("%s: %s" % (key, value))

#ACDC/Ballbreaker', 'Hard as a Rock
#client.add("ACDC/Ballbreaker/16-01 Hard As A Rock.mp3")

#client.play()


current_song = client.currentsong()
status = client.status()
stats = client.stats()

sys.stdout.write('{')
sys.stdout.write('"status":{}'.format(status))
sys.stdout.write(',')
sys.stdout.write('"current_song": {}'.format(current_song))
print "}\n"
#print "Stats: {}".format(stats);

