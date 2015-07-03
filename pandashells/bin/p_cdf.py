#! /usr/bin/env python

# standard library imports
import argparse

import sys  # NOQA  need this for mock testig

from pandashells.lib import module_checker_lib, arg_lib, io_lib, plot_lib

# import required dependencies
modulesOkay = module_checker_lib.check_for_modules([
    'pandas',
    'numpy',
    'matplotlib',
    'statsmodels'
])

import pandas as pd
import numpy as np
import pylab as pl
from statsmodels.distributions.empirical_distribution import ECDF


def main():
    msg = "Plot cumulative distribution of input column."

    # read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    arg_lib.add_args(parser, 'io_in', 'io_out', 'example', 'decorating')

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
