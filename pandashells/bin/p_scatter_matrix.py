#! /usr/bin/env python

# standard library imports
import argparse
import sys  # NOQA  need this for testing but not used in this code

from pandashells.lib import module_checker_lib, arg_lib, io_lib, plot_lib

# import required dependencies
module_checker_lib.check_for_modules(['pandas', 'matplotlib'])

import pandas as pd


def main():
    msg = "Create a matrix of scatter plots to show correlation between "
    msg += "specified columns."

    # read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    arg_lib.add_args(parser, 'io_in', 'example', 'decorating')

    # specify columns
    parser.add_argument("-c", "--cols",
                        help="Column(s) to correlate", nargs="+")

    # specify opacity
    parser.add_argument("-a", "--alpha", help="Set opacity",
                        nargs=1, default=[0.5], type=float)

    # parse arguments
    args = parser.parse_args()

    # get the input dataframe
    df = io_lib.df_from_input(args)

    # extract parameters from arg parser
    if args.cols:
        cols = args.cols
    else:
        cols = list(df.columns)

    # make sure all columns exist in dataframe
    bad_col_list = [c for c in cols if c not in df.columns]
    if bad_col_list:
        msg = "\n\nThese columns were not found:\n\t"
        msg += ",\n\t".join(bad_col_list)
        raise ValueError(msg)

    # set the appropriate theme
    plot_lib.set_plot_styling(args)

    # create the scatter matrix
    df = df[cols]
    pd.tools.plotting.scatter_matrix(df, alpha=args.alpha[0])
    plot_lib.show(args)


if __name__ == '__main__':  # pragma: no cover
    main()
