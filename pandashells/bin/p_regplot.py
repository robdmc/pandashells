#! /usr/bin/env python

# standard library imports
import argparse
import re
import sys  # NOQA just use this for patching in tests

from pandashells.lib import module_checker_lib, arg_lib, io_lib, plot_lib

# import required dependencies
module_checker_lib.check_for_modules(
    ['pandas', 'numpy', 'matplotlib', 'seaborn'])

import numpy as np
import matplotlib as mpl
import pylab as pl
import seaborn as sns

sns.set_context('talk')
CC = mpl.rcParams['axes.color_cycle']


def make_label(coeffs, savefig):
    label_plain = 'y = '
    for nn, coeff in enumerate(coeffs[::-1]):
        if nn > 0:
            label_plain += ' + '
        if nn == 0:
            label_plain += '(%0.4g)' % coeff
        elif nn == 1:
            label_plain += '(%0.4g) x' % coeff
        else:
            label_plain += '(%0.4g) x ^ %d' % (coeff, nn)
    label_tex = '${}$'.format(label_plain)
    label = label_tex
    if savefig:
        if re.compile(r'.*?\.html$').match(savefig[0]):
            label = label_plain
    return label


def main():
    msg = 'Shows a quick single variable regression plot of specified order.'

    # read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    arg_lib.add_args(parser, 'io_in', 'io_out', 'example', 'decorating')

    msg = 'Column for dependent variable'
    parser.add_argument('-x', nargs=1, type=str, dest='x', metavar='col',
                        help=msg, required=True)

    msg = 'Column for independent variable'
    parser.add_argument('-y', nargs=1, type=str, dest='y',
                        metavar='col', help=msg, required=True)

    msg = 'The order of the polynomial to fit (default = 1)'
    parser.add_argument('--order', help=msg, nargs=1, default=[1], type=int)

    msg = 'Number of bootstrap samples for uncertainty region (default=1000)'
    parser.add_argument(
        '--n_boot', help=msg, nargs=1, default=[1000], type=int)

    parser.add_argument('-a', '--alpha', help='Set opacity',
                        nargs=1, default=[0.5], type=float)

    # parse arguments
    args = parser.parse_args()

    # get the input dataframe
    df = io_lib.df_from_input(args)

    # extract command line params
    x = df[args.x[0]].values
    y = df[args.y[0]].values

    # do a polyfit with the specified order
    coeffs = np.polyfit(x, y, args.order[0])

    label = make_label(coeffs, args.savefig)

    sns.regplot(
        x, y, order=args.order[0], n_boot=args.n_boot[0],
        line_kws={'label': label, 'color': CC[2], 'alpha': .5},
        scatter_kws={'alpha': args.alpha[0], 'color': CC[0]})

    pl.legend(loc='best')
    pl.xlabel(args.x[0])
    pl.ylabel(args.y[0])
    plot_lib.refine_plot(args)
    plot_lib.show(args)


if __name__ == '__main__':  # pragma: no cover
    main()
