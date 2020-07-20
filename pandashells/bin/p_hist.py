#! /usr/bin/env python

# standard library imports
import sys
import argparse
import importlib
import textwrap

from pandashells.lib import module_checker_lib, arg_lib

module_checker_lib.check_for_modules(['pandas'])
from pandashells.lib import io_lib

import numpy as np
import pandas as pd


# this silly function makes mock testing easier
def get_imports(name):  # pragma no cover
    return importlib.import_module(name)


def get_input_args():
    msg = textwrap.dedent(
        """
        Plot histograms from input data.  Can either plot just a single
        histogram or a grid of histograms with different columns of data.
        When multiple columns are specified, creates a grid of histograms,
        one for each specified column.

        -----------------------------------------------------------------------
        Examples:

            * Plot histogram of a beta distriubtion
                p.rand -t beta --alpha 3 --beta 10 -n 10000\\
                | p.hist --names beta -n 50

            * Plot a sid-by-side comparison of a gamma and normal distriubtion
              paste <(p.rand -t normal  -n 10000 | p.df --names normal)\\
                    <(p.rand -t gamma   -n 10000 | p.df --names gamma)\\
              | p.hist -i table -c normal gamma
        -----------------------------------------------------------------------
        """
    )

    #  read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    arg_lib.add_args(parser, 'io_in', 'io_out', 'decorating')

    # specify columns to histogram
    parser.add_argument(
        '-c', '--cols', help='Column(s) to histogram', nargs='+')
    parser.add_argument(
        '-q', '--quiet', action='store_true', default=False,
        help='Quiet mean no plots. Send numeric output to stdout instead')
    parser.add_argument(
        '-n', '--nbins', help='Number of bins (default=30)', nargs=1,
        default=[30], type=int)
    parser.add_argument(
        '-r', '--range', help='Range (min max) of x axis', nargs=2,
        default=None, type=float)
    parser.add_argument(
        '-l', '--layout', help='Layout (rows, cols)',
        nargs=2, default=None, type=int)
    parser.add_argument(
        '-a', '--alpha', help='Set opacity of hist bars', nargs=1,
        default=[1.], type=float)
    parser.add_argument(
        '-d', '--density', action='store_true', default=False,
        help='Show probability density instead of counts')
    parser.add_argument(
        '--sharex', action='store_true', default=False,
        help='Make all x axes have the same range')
    parser.add_argument(
        '--sharey', action='store_true', default=False,
        help='Make all y axes have the same range')
    return parser.parse_args()


def validate_args(args, cols, df):
    # make sure all columns exist in dataframe
    bad_col_list = [c for c in cols if c not in df.columns]
    if bad_col_list:
        msg = '\n\nThese columns were not found:\n\t'
        msg += ',\n\t'.join(bad_col_list)
        sys.stderr.write(msg + '\n')
        sys.exit(1)

    if args.quiet and len(cols) > 1:
        msg = "Quiet is only allowed for single histograms"
        sys.stderr.write(msg)
        sys.exit(1)


def main():
    args = get_input_args()
    df = io_lib.df_from_input(args)

    # extract parameters from arg parser
    nbins = args.nbins[0]
    range_tup = args.range
    layout_tup = args.layout
    alpha = args.alpha[0]
    do_density = args.density
    sharex = args.sharex
    sharey = args.sharey
    cols = args.cols if args.cols else [df.columns[0]]

    validate_args(args, cols, df)

    # no plotting if output requested
    if args.quiet:
        counts, edges = np.histogram(
            df[cols[0]], bins=nbins, range=range_tup, density=do_density)
        centers = edges[:-1] + 0.5 * np.diff(edges)
        df_out = pd.DataFrame({'bins': centers, 'counts': counts})
        io_lib.df_to_output(args, df_out)

    # otherwise do plotting
    else:
        module_checker_lib.check_for_modules(['matplotlib'])
        plot_lib = get_imports('pandashells.lib.plot_lib')
        plot_lib.set_plot_styling(args)
        df.hist(cols, bins=nbins, range=range_tup,
                alpha=alpha, sharex=sharex, sharey=sharey, layout=layout_tup,
                density=do_density)

        plot_lib.refine_plot(args)
        plot_lib.show(args)


if __name__ == '__main__':  # pragma: no cover
    main()
