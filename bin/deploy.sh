#!/bin/bash
cd /home/jw/python/workspace/elevenbits
rm -rf /tmp/elevenbits
mkdir /tmp/elevenbits
svn export . /tmp/elevenbits --force
scp -r /tmp/elevenbits jw@elevenbits.com:/home/jw/


 