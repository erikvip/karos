#!/bin/bash
#python ./mpd-test.py | cut -d' ' -f2- | sed "s/u'/'/g" | tr "'" '"' | jq -C .
python ./mpd-test.py | sed "s/u'/'/g" | tr "'" '"' | jq -C .
