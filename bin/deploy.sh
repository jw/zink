#!/bin/bash
rmdir /tmp/elevenbits
mkdir /tmp/elevenbits
svn export . /svn/elevenbits
scp -r /svn/elevenbits jw@elevenbits.com:/home/jw/


 