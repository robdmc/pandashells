#! /usr/bin/env python

import argparse
import sys
import textwrap

from pandashells.lib import arg_lib, module_checker_lib
module_checker_lib.check_for_modules(['pandas'])
from pandashells.lib import io_lib


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
    msg = textwrap.dedent(
        """
        Create strings from a dataframe using python str.format() template.
        This tool is particularly useful for generating a list of commands
        that for piping into p.parallel.
        -----------------------------------------------------------------------
        Examples:

            * Create commands to touch a sequence of files in /tmp
                seq 10 | p.df --names n -i noheader\\
                | p.format -t 'touch /tmp/file{n:02d}.txt'
        -----------------------------------------------------------------------
        """
    )

    #  read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

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
