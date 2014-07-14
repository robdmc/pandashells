#! /usr/bin/env python

#--- standard library imports
import os
import sys
import argparse
import re

############# dev only.  Comment out for production ######################
sys.path.append('../..')
##########################################################################

from pandashells.lib import module_checker_lib, arg_lib, io_lib, plot_lib

#--- import required dependencies
modulesOkay = module_checker_lib.check_for_modules(
        [
            'pandas',
            'matplotlib',
        ])
if not modulesOkay:
    sys.exit(1)

import pandas as pd
import matplotlib as mpl
import pylab as pl

#=============================================================================
if __name__ == '__main__':
    msg = "Write "
    msg += "something here"

    #--- read command line arguments
    parser = argparse.ArgumentParser(
            description=msg)

    arg_lib.addArgs(parser, 'io_in', 'xy_plotting', 'decorating', 'example',
            io_no_col_spec_allowed=False)

    parser.add_argument("-a", "--alpha", help="Set opacity",
            nargs=1, default=[1.], type=float)


    #--- parse arguments
    args = parser.parse_args()

    #--- get the input dataframe
    df = io_lib.df_from_input(args)

    #--- set the appropriate theme
    plot_lib.set_plot_styling(args)

    #--- draw the plot
    plot_lib.draw_xy_plot(args, df)
