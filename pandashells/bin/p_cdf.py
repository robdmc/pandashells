#! /usr/bin/env python

# standard library imports
import argparse
import textwrap
import warnings

import sys  # NOQA  need this for mock testig

from pandashells.lib import module_checker_lib

# import required dependencies
module_checker_lib.check_for_modules([
    'pandas',
    'numpy',
    'matplotlib',
    'statsmodels'
])
from pandashells.lib import arg_lib, io_lib, plot_lib

import pandas as pd
import numpy as np

warnings.filterwarnings('ignore')
import pylab as pl
warnings.resetwarnings()
from statsmodels.distributions.empirical_distribution import ECDF


def main():
    msg = textwrap.dedent(
        """
        Plots the emperical cumulative distribution function (ECDF).

        -----------------------------------------------------------------------
        Examples:

            * Plot ECDF for 10k samples from the standard normal distribution.
                p.rand -t normal -n 10000 | p.cdf -c c0

            * Instead of plotting, send ECDF values to stdout
                p.rand -t normal -n 10000 | p.cdf -c c0 -q | head
        -----------------------------------------------------------------------
        """
    )

    # read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    # specify column to use
    parser.add_argument(
        "-c", "--col", required=True, nargs=1,
        help="Column to plot distribution")
    parser.add_argument(
        '-n', '--n_points', nargs=1, type=int,
        help='Number of output points (default is twice input len)')
    parser.add_argument(
        '-q', '--quiet', action='store_true', default=False,
        help='Quiet mean no plots. Send numeric output to stdout instead')

    # parse arguments
    arg_lib.add_args(parser, 'decorating', 'io_in', 'io_out',)
    args = parser.parse_args()

    # get the input dataframe and extract column
    df = io_lib.df_from_input(args)
    x = df[args.col[0]].values

    # create the output distribution
    n_out = 2 * len(x) if args.n_points is None else args.n_points[0]
    x_out = np.linspace(min(x), max(x), n_out)
    y_out = ECDF(x)(x_out)

    # send values to stdout if quiet specified
    if args.quiet:
        df_out = pd.DataFrame(
            {'x': x_out, 'p_less': y_out, 'p_greater': 1 - y_out})
        df_out = df_out[['x', 'p_less', 'p_greater']]
        io_lib.df_to_output(args, df_out)
        return

    # set the appropriate theme ad make plot
    plot_lib.set_plot_styling(args)
    pl.plot(x_out, y_out, label='P({} < x)'.format(args.col[0]))
    pl.plot(x_out, 1. - y_out, label='P({} > x)'.format(args.col[0]))
    pl.xlabel('x')
    pl.legend(loc='best')

    plot_lib.refine_plot(args)
    plot_lib.show(args)


if __name__ == '__main__':  # pragma: no cover
    main()
