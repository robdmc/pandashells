#! /usr/bin/env python

import argparse
import sys

from pandashells.lib import arg_lib, io_lib


class OutStream(object):  # pragma no cover
    """
    This class exisist for easing testing of sys.stdout and doesn't
    need to be tested itself
    """
    def __init__(self, template):
        self.template = template

    def write(self, **kwargs):
        sys.stdout.write(self.template.format(**kwargs) + '\n')


def main():
    msg = (
        'Use python template to create strings from dataframe '
        'records.  Each record will get past as **kwargs to the python '
        '.format(**kwargs) string method.'
    )

    # read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    arg_lib.add_args(parser, 'io_in')

    parser.add_argument('-t', '--template', required=True,
                        help='A python template string', nargs=1)

    # parse arguments
    args = parser.parse_args()

    # get the input dataframe
    df = io_lib.df_from_input(args)

    # write out the strings
    stream = OutStream(args.template[0])
    for rec in df.to_dict('records'):
        stream.write(**rec)


if __name__ == '__main__':  # pragma: no cover
    main()
