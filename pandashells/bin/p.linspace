#! /usr/bin/env python

# --- standard library imports
import os
import sys
import argparse
import re

from pandashells.lib import module_checker_lib, arg_lib, io_lib

# --- import required dependencies
modulesOkay = module_checker_lib.check_for_modules(['numpy', 'pandas'])
if not modulesOkay:
    sys.exit(1)

import numpy as np
import pandas as pd

# =============================================================================
if __name__ == '__main__':
    msg = "Generate a linearly spaced set of data points."

    # --- read command line arguments
    msg = 'p.linspace start end npoints [-h] '
    msg += '[-o option [option ...]] [--example]'
    parser = argparse.ArgumentParser(description=msg, usage=msg)

    arg_lib.addArgs(parser, 'io_out', 'example')

    msg = 'start end npoints'
    parser.add_argument("numbers", help=msg, type=int, nargs=3, metavar='')

    # --- parse arguments
    args = parser.parse_args()

    df = pd.DataFrame({'c0': np.linspace(*args.numbers)})

    # --- write dataframe to output
    io_lib.df_to_output(args, df)
