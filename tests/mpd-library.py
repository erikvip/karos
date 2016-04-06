#!/usr/bin/python
import mpd
import sys
client = mpd.MPDClient()
client.connect("localhost", 6600)

info = client.lsinfo("/");
print info

for entry in info:
    print entry

