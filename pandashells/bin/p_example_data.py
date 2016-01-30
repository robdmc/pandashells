#! /usr/bin/env python

# standard library imports
import os
import sys  # noqa
import argparse
import textwrap

import pandashells


def main():
    # create a dict of data-set names and corresponding files
    package_dir = os.path.dirname(os.path.realpath(pandashells.__file__))
    sample_data_dir = os.path.realpath(
        os.path.join(package_dir, 'example_data'))

    f_dict = {}
    for f in os.listdir(sample_data_dir):
        f_dict[f.replace('.csv', '')] = os.path.join(sample_data_dir, f)

    # read command line arguments
    msg = textwrap.dedent(
        """
        Provides access to sample csv data sets for exploring the pandashells
        toolkit.

        -----------------------------------------------------------------------
        Examples:

        * Restaraunt tips along with patron information.
             p.example_data -d tips | head

        * Relative rise in global sea surface height over the past couple
          decades.  Original source: http://sealevel.colorado.edu/
             p.example_data -d sealevel | head

        * Polling data for 2008 US presidential
             p.example_data -d election | head

        * US Electoral college and population numbers by state
             p.example_data -d electoral_college | head
        -----------------------------------------------------------------------
        """
    )

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    parser.add_argument(
        '-d', '--dataset', nargs=1, type=str,
        dest='dataset', choices=sorted(f_dict.keys()), required=True,
        help='The name of the sample dataset')

    # parse arguments
    args = parser.parse_args()

    # print contents of data file to output
    f_name = f_dict[args.dataset[0]]
    with open(f_name) as in_file:
        try:
            # line by line avoids weird sys.excepthook bug on pipe to head
            for line in in_file:
                sys.stdout.write(line.strip() + '\n')
        except IOError:
            pass

    # weird warning on python3 is fixed by closing stdout
    try:
        sys.stdout.close()
    except IOError:
        pass


if __name__ == '__main__':  # pragma: no cover
    main()
