#! /usr/bin/env python

#--- standard library imports
import os
import sys
import argparse

############# dev only.  Comment out for production ######################
sys.path.append('../..')
##########################################################################


from ptools.lib import module_checker_lib, arg_lib

#--- import required dependencies
modulesOkay = module_checker_lib.check_for_modules(
        [
            'pandas',
            'numpy',
            'scipy',
        ])
if not modulesOkay:
    sys.exit(1)
import pandas as pd

if __name__ == '__main__':
    msg = "Bring pandas manipulation to command line.  Input from stdin "
    msg += "is placed into a dataframe named 'df'.  The output of all "
    msg += "specified commands must evaluate to a dataframe that will also "
    msg += "be named 'df'. The output of the final command will be sent "
    msg += "to stdout."


    #--- read command line arguments
    parser = argparse.ArgumentParser(
            description=msg)

    arg_lib.addArgs(parser, 'csv', 'example')
    parser.add_argument("statement", help="Statement to execute", nargs="+")


    #--- parse arguments
    args = parser.parse_args()







#print pd
#print 'running code'
##print 'done'
#
#
#"""
#Need to figure out csv reading arguments
#
#
#
#p.df -i [csv|table|raw] -o [csv|table|raw]  f
#"""
