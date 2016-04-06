#!/usr/bin/python
import mpd
import sys
client = mpd.MPDClient()
client.connect("localhost", 6600)

current_song = client.currentsong()
status = client.status()
stats = client.stats()

sys.stdout.write('{')
sys.stdout.write('"status":{}'.format(status))
sys.stdout.write(',')
sys.stdout.write('"current_song": {}'.format(current_song))
print "}\n"

