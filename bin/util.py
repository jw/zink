#!/usr/bin/python

from svn import core 

from os import remove, rmdir, listdir
from os.path import exists, isfile, isdir, join

def get_svn_errors():
    errors = {}
    for key in vars(core):
        if key.find('SVN_ERR_') == 0:
            try:
                val = int(vars(core)[key])
                errors[val] = key
            except:
                pass
    return errors

def removedirs(path):
    
    print "Removing " + path
    
    if exists(path):
        print "Preparing to remove: " + str(path)
        list = listdir(path)
        for file in list:
            print "removing " + file
            full = join(path, file)
            if isdir(full):                
                print "Removing files in " + full + "..."
                removedirs(full)
                print "Removing dir..."
                rmdir(full)
            else:
                print "Removing file..."
                remove(full)
