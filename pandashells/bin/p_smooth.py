#! /usr/bin/env python

# standard library imports
import sys
import argparse
import importlib
import textwrap

from pandashells.lib import module_checker_lib, arg_lib

module_checker_lib.check_for_modules(['pandas', 'supersmoother'])
from supersmoother import SuperSmoother
from pandashells.lib import io_lib

import numpy as np


# this silly function makes mock testing easier
def get_imports(name):  # pragma no cover
    return importlib.import_module(name)


def get_input_args():
    msg = textwrap.dedent(
        """
        Smooths data in specified column.  Uses algorithm[1] from the
        supersmoother python package for smoothing with cross validation
        to determine best span.

        [1] Friedman, J. H. (1984) A variable span scatterplot smoother.
            Laboratory for Computational Statistics, Stanford University
            Technical Report No. 5.
            pdf: http://www.slac.stanford.edu/cgi-wrap/getdoc/slac-pub-3477.pdf


        -----------------------------------------------------------------------
        Examples:

           * Smooth sea level time series
                 p.example_data -d sealevel \\
                 | p.df 'df["smoothed"] = df.sealevel_mm' \\
                 | p.smooth -x year -y smoothed \\
                 | p.plot -x year -y sealevel_mm smoothed \\
                   --legend best -s .  '-' --alpha .5 1

           * Now pretend year doesn't exist and treat as equally spaced
                 p.example_data -d sealevel \\
                 | p.df 'df["smoothed"] = df.sealevel_mm' \\
                 | p.smooth -y smoothed \\
                 | p.plot -x year -y sealevel_mm smoothed \\
                   --legend best -s .  '-' --alpha .5 1
        -----------------------------------------------------------------------
        """
    )

    #  read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    arg_lib.add_args(parser, 'io_in', 'io_out')

    # specify columns to histogram
    parser.add_argument(
        '-y', dest='y', help='Column(s) to smooth', nargs='+', required=True)
    parser.add_argument(
        '-x', dest='x', help='Optional: if y=f(x), specify x', nargs=1)
    return parser.parse_args()


def validate_args(args, cols, df):
    # make sure all columns exist in dataframe
    bad_col_list = [c for c in cols if c not in df.columns]
    if bad_col_list:
        msg = '\n\nThese columns were not found:\n\t'
        msg += ',\n\t'.join(bad_col_list)
        sys.stderr.write(msg + '\n')
        sys.exit(1)


def smooth(df, columns, x_col=None):
    model = SuperSmoother()

    x = df[x_col] if x_col else np.arange(len(df))
    for col in columns:
        y = df[col].values
        model.fit(x, y)
        df[col] = model.predict(x)
    return df


def main():
    args = get_input_args()
    df = io_lib.df_from_input(args)

    # extract parameters from arg parser
    x_col = args.x[0] if args.x else None
    cols = args.y if args.y else [df.columns[0]]
    cols_to_check = cols + [x_col] if x_col else cols
    validate_args(args, cols_to_check, df)
    df = smooth(df, cols, x_col)
    io_lib.df_to_output(args, df)


if __name__ == '__main__':  # pragma: no cover
    main()
