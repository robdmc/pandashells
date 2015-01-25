#! /usr/bin/env python

# --- standard library imports
import os
import sys
import argparse
import re

from pandashells.lib import module_checker_lib, arg_lib, io_lib, plot_lib

# --- import required dependencies
modulesOkay = module_checker_lib.check_for_modules(['pandas', 'matplotlib'])
if not modulesOkay:
    sys.exit(1)

import pandas as pd
import matplotlib as mpl
import pylab as pl

# ============================================================================
if __name__ == '__main__':
    msg = "Plot histograms from input data.  Can either plot just a single "
    msg += "histogram or a grid of histograms with different columns of "
    msg += "data.  When multiple columns are specified, creates a grid of "
    msg += "histograms, one for each specified column."

    # --- read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    arg_lib.addArgs(parser, 'io_in', 'example', 'decorating',
                    io_no_col_spec_allowed=False)

    #WANT TO ADD A -o OPTION TO THIS TO OUTPUT BIN COUNTS
    # --- specify columns to histogram
    parser.add_argument("-c", "--cols",
                        help="Column(s) to histogram", nargs="+")

    parser.add_argument("-n", "--nbins", help="Number of bins (default=30)",
                        nargs=1, default=[30], type=int)
    parser.add_argument("-r", "--range", help="Range (min max) of x axis",
                        nargs=2, default=None, type=float)
    parser.add_argument("-l", "--layout", help="Layout (rows, cols)",
                        nargs=2, default=None, type=int)
    parser.add_argument("-a", "--alpha", help="Set opacity of hist bars",
                        nargs=1, default=[1.], type=float)
    parser.add_argument("-d", "--density", action="store_true", default=False,
                        help="Show probability density instead of counts")
    parser.add_argument("--sharex", action="store_true", default=False,
                        help="Make all x axes have the same range")
    parser.add_argument("--sharey", action="store_true", default=False,
                        help="Make all y axes have the same range")

    # --- parse arguments
    args = parser.parse_args()

    # --- get the input dataframe
    df = io_lib.df_from_input(args)

    # --- extract parameters from arg parser
    nbins = args.nbins[0]
    range_tup = args.range
    layout_tup = args.layout
    alpha = args.alpha[0]
    do_density = args.density
    sharex = args.sharex
    sharey = args.sharey
    if args.cols:
        cols = args.cols
    else:
        cols = [df.columns[0]]

    # --- make sure all columns exist in dataframe
    bad_col_list = [c for c in cols if c not in df.columns]
    if bad_col_list:
        msg = "\n\nThese columns were not found:\n\t"
        msg += ",\n\t".join(bad_col_list)
        sys.stderr.write(msg+'\n')
        sys.exit(1)

    # --- set the appropriate theme
    plot_lib.set_plot_styling(args)

    df.hist(cols, bins=nbins, range=range_tup,
            alpha=alpha, sharex=sharex, sharey=sharey, layout=layout_tup,
            normed=do_density)

    plot_lib.refine_plot(args)
    plot_lib.show(args)
