#! /usr/bin/env python

# --- standard library imports
import os
import sys
import argparse
import re

# ############ dev only.  Comment out for production ######################
sys.path.append('../..')
# #########################################################################

from pandashells.lib import module_checker_lib, arg_lib, io_lib, plot_lib

# --- import required dependencies
modulesOkay = module_checker_lib.check_for_modules([
    'pandas',
    'matplotlib',
    'scipy'
])
if not modulesOkay:
    sys.exit(1)

import pandas as pd
import matplotlib as mpl
import pylab as pl
import scipy as scp

# ============================================================================
if __name__ == '__main__':
    msg = "Plot cumulative distribution of input column."

    # --- read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    arg_lib.addArgs(parser, 'io_in', 'example', 'decorating',
                    io_no_col_spec_allowed=False)

    # --- specify columns to histogram
    parser.add_argument("-c", "--col",
                        help="Column to plot distribution", nargs=1)

    # --- parse arguments
    args = parser.parse_args()

    # --- get the input dataframe and extract column
    df = io_lib.df_from_input(args)
    if args.col is None:
        args.col = [df.columns[0]]

    x = df[args.col[0]].values

    # --- set the appropriate theme
    plot_lib.set_plot_styling(args)

    # --- compute and plot the cdf
    osm, osr = scp.stats.probplot(x, dist='uniform', fit=False)
    pl.plot(osr, osm, label='P({} < x)'.format(args.col[0]))
    pl.plot(osr, 1 - osm, label='P({} > x)'.format(args.col[0]))
    pl.xlabel('x')
    pl.legend(loc='best')

    plot_lib.refine_plot(args)
    plot_lib.show(args)
