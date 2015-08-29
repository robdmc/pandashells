#! /usr/bin/env python

# standard library imports
import argparse
import textwrap
import sys  # NOQA  importing sys so I can mock sys.argv in tests

from pandashells.lib import module_checker_lib, arg_lib

module_checker_lib.check_for_modules(['pandas'])
from pandashells.lib import io_lib

import pandas as pd
import numpy as np


# want different default mu values for normal and poisson distributions
def fill_default_mu(args):
    if args.type[0] == 'normal':
        args.mu = [0.] if args.mu is None else args.mu
    elif args.type[0] == 'poisson':
        args.mu = [1.] if args.mu is None else args.mu
    return args


def get_samples(args):
    """
    Return samples from selected distribution
    """

    # dictionary to hold numpy arguments for different distributions
    distribution_for = {
        'uniform': {
            'function': np.random.uniform,
            'kwargs': {
                'low': args.min[0],
                'high': args.max[0],
                'size': (args.num_samples[0], args.columns[0]),
            },
        },
        'normal': {
            'function': np.random.normal,
            'kwargs': {
                'loc': args.mu[0] if args.mu else None,
                'scale': args.sigma[0],
                'size': (args.num_samples[0], args.columns[0]),
            },
        },
        'poisson': {
            'function': np.random.poisson,
            'kwargs': {
                'lam': args.mu[0] if args.mu else None,
                'size': (args.num_samples[0], args.columns[0]),
            },
        },
        'beta': {
            'function': np.random.beta,
            'kwargs': {
                'a': args.alpha[0],
                'b': args.beta[0],
                'size': (args.num_samples[0], args.columns[0]),
            },
        },
        'gamma': {
            'function': np.random.gamma,
            'kwargs': {
                'shape': args.alpha[0],
                'scale': 1. / args.beta[0],
                'size': (args.num_samples[0], args.columns[0]),
            },
        },
        'binomial': {
            'function': np.random.binomial,
            'kwargs': {
                'n': args.N[0],
                'p': args.p[0],
                'size': (args.num_samples[0], args.columns[0]),
            },
        },

    }

    # grab the function for generating proper distribution
    dist = distribution_for[args.type[0]]

    # call the random generating function with the proper kwargs
    values = dist['function'](**dist['kwargs'])

    # set column names of output dataframe
    columns = ['c{}'.format(c) for c in range(args.columns[0])]

    # framify and return results
    return pd.DataFrame(values, columns=columns)


def main():
    msg = textwrap.dedent(
        """
        Return random samples from common probability distrubtions.

        -----------------------------------------------------------------------
        Examples:

            uniform:  p.rand -n 1000 -t uniform  --min=0    --max=1   | p.hist
            normal:   p.rand -n 1000 -t normal   --mu=0     --sigma=1 | p.hist
            poisson:  p.rand -n 1000 -t poisson  --mu=1               | p.hist
            beta:     p.rand -n 1000 -t beta     --alpha=2  --beta=6  | p.hist
            gamma:    p.rand -n 1000 -t gamma    --alpha=1  --beta=1  | p.hist
            binomial: p.rand -n 1000 -t binomial --N=10     --p=0.4   | p.hist
        -----------------------------------------------------------------------
        """
    )

    # read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    parser.add_argument(
        '-t', '--type', nargs=1, type=str, default=['uniform'],
        choices=['uniform', 'normal', 'beta', 'gamma', 'binomial', 'poisson'],
        help='type of distribution (default=\'uniform\')')
    parser.add_argument(
        '-n', '--num_samples', nargs=1, default=[10], type=int,
        help='The number of rows to generate (default=10)')
    parser.add_argument(
        '-c', '--columns', nargs=1, default=[1], type=int,
        help='The number of columns to generate per row (default=1)')
    parser.add_argument(
        '--N', nargs=1, default=[10], type=int,
        help=(
            '(Binomial Dist) Largest possible value for random variable. '
            '(default=10)'
        )
    )
    parser.add_argument(
        '--p', nargs=1, default=[.5], type=float,
        help=(
            '(Binomial Dist) Bernoulli probability for each trial'
            '(default=.5)'
        )
    )
    parser.add_argument(
        '--mu', nargs=1, type=float,
        help='(Normal, Poisson) Mean (defaults: normal:0, poisson:1')
    parser.add_argument(
        '--sigma', nargs=1, default=[1.], type=float,
        help='(Normal) standard deviation, (default: 1)')
    parser.add_argument(
        '--min', nargs=1, default=[0.], type=float,
        help='(Uniform) Minimum value of range, (default: 0)')
    parser.add_argument(
        '--max', nargs=1, default=[1.], type=float,
        help='(Uniform) Maximum value of range, (default: 1)')
    parser.add_argument(
        '--alpha', nargs=1, default=[2.], type=float,
        help='(Beta, Gamma)  (default: 2)')
    parser.add_argument(
        '--beta', nargs=1, default=[2.], type=float,
        help='(Beta, Gamma)  (default: 2)')

    arg_lib.add_args(parser, 'io_out')

    # parse arguments
    args = parser.parse_args()

    # set some defaults
    args = fill_default_mu(args)

    # get the samples
    df = get_samples(args)

    # write dataframe to output
    io_lib.df_to_output(args, df)

if __name__ == '__main__':  # pragma: no cover
    main()
