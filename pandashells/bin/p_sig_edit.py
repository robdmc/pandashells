#! /usr/bin/env python

# --- standard library imports
import os
import sys
import argparse
import re

from pandashells.lib import module_checker_lib, arg_lib, io_lib

# --- import required dependencies
modulesOkay = module_checker_lib.check_for_modules(['pandas', 'numpy'])
if not modulesOkay:
    sys.exit(1)

import pandas as pd
import numpy as np

# ============================================================================
if __name__ == '__main__':
    msg = "Perform recursive sigma editing on columns of a dataframe. "
    msg += "Recursively NaNs out values greater than sigma_thresh standard "
    msg += "deviations away from sample mean."

    # --- read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    options = {}
    arg_lib.addArgs(parser, 'io_in', 'io_out', 'example',
                    io_no_col_spec_allowed=True)
    parser.add_argument("-t", "--sigma_thresh", help="Sigma threshold",
                        nargs=1, required=True, type=float)
    parser.add_argument("-c", "--cols", required=True,
                        help="Column(s) to sigma-edit", nargs="+")

    # --- parse arguments
    args = parser.parse_args()

    # --- get the input dataframe
    df = io_lib.df_from_input(args)

    # --- define function to perform one sigma-edit pass
    def single_pass(in_series, sigma_thresh):
        if in_series.count() == 0:
            msg = "Error:  All values edited out.  Try "
        needs_another_pass = False
        mu = in_series.mean()
        resid = in_series - mu
        std = in_series.std()
        sigma_t = sigma_thresh * std
        outside = resid.abs() > sigma_t

        if sum(outside) > 0:
            needs_another_pass = True
        in_series[outside] = np.NaN
        return needs_another_pass, in_series

    # --- sigma-edit each column
    for col_name in args.cols:
        needs_another_pass = True
        ser = df[col_name]
        while needs_another_pass:
            needs_another_pass, ser = single_pass(ser, args.sigma_thresh[0])
        df[col_name] = ser

    # --- write dataframe to output
    io_lib.df_to_output(args, df)