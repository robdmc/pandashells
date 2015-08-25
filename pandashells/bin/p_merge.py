#! /usr/bin/env python

# standard library imports
import sys
import argparse
import textwrap

from pandashells.lib import module_checker_lib, arg_lib

# import required dependencies
module_checker_lib.check_for_modules(['pandas'])
from pandashells.lib import io_lib

import pandas as pd


def validate_args(args):
    # make sure join criteria are properly specified
    if (args.left_on is None) and not (args.right_on is None):
        msg = '\nMust specify both left_on and right_on '
        msg += 'if either is specified\n\n'
        sys.stderr.write(msg)
        sys.exit(1)
    if (args.right_on is None) and not (args.left_on is None):
        msg = '\nMust specify both left_on and right_on '
        msg += 'if either is specified\n\n'
        sys.stderr.write(msg)
        sys.exit(1)
    if (args.right_on is None) and (args.left_on is None) and \
            (args.on is None):
        msg = '\nMust specify a join criteria\n\n'
        sys.stderr.write(msg)
        sys.exit(1)
    if not (args.left_on is None):
        args.on = None


def main():
    msg = textwrap.dedent(
        """
        Tool to merge datasets.  Similar functionality to database
        joins. The arguments closely parallel those of the pandas merge
        command.  See the pandas merge documentation for more details.

        -----------------------------------------------------------------------
        Examples:

            * Merge election polls with electoral-college numbers
                p.merge <(p.example_data -d election) \\
                        <(p.example_data -d electoral_college) \\
                        --how left --on state \\
                | p.df -o table | head
        -----------------------------------------------------------------------
        """
    )

    # read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    arg_lib.add_args(parser, 'io_in', 'io_out')

    parser.add_argument('--how', choices=['left', 'right', 'inner', 'outer'],
                        dest='how', default=['inner'], nargs=1,
                        help="Type of join.  Default='inner'")

    msg = 'List of of columns on which to join'
    parser.add_argument('--on', nargs='+', metavar='col',
                        type=str, dest='on', help=msg)

    msg = 'List of of columns from left file to join on. '
    parser.add_argument('--left_on', nargs='+', metavar='col',
                        type=str, dest='left_on', help=msg)

    msg = 'List of of columns from right file to join on. '
    parser.add_argument('--right_on', nargs='+', metavar='col',
                        type=str, dest='right_on', help=msg)

    msg = 'List of suffixes appended to identically '
    msg += 'named columns'
    parser.add_argument('--suffixes', nargs=2, metavar='_x _y',
                        type=str, dest='suffixes', default=['_x', '_y'],
                        help=msg)

    parser.add_argument("file", help="Files to join", nargs=2, type=str,
                        metavar='file')

    args = parser.parse_args()
    validate_args(args)

    # get merge options from cli
    how = args.how[0]
    on = args.on if args.on else None
    left_on = args.left_on if args.left_on else None
    right_on = args.right_on if args.right_on else None
    suffixes = args.suffixes

    # get file names
    left_name, right_name = tuple(args.file)

    # load the dataframes
    df_left = io_lib.df_from_input(args, left_name)
    df_right = io_lib.df_from_input(args, right_name)

    # perform the merge
    dfj = pd.merge(df_left, df_right, how=how, on=on, left_on=left_on,
                   right_on=right_on, sort=True, suffixes=suffixes)

    # output the joined frame
    io_lib.df_to_output(args, dfj)


if __name__ == '__main__':  # pragma: no cover
    main()
