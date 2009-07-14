#!/usr/bin/python

from svn import core 

def get_svn_errors():
    errs = {}
    for key in vars(core):
        if key.find('SVN_ERR_') == 0:
            try:
                val = int(vars(core)[key])
                errs[val] = key
            except:
                pass
    return errs

