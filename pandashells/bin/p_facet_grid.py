#! /usr/bin/env python

# standard library imports
import argparse
import sys  # NOQA just use this for patching in tests
import textwrap
import warnings
warnings.filterwarnings('ignore')

from pandashells.lib import module_checker_lib, arg_lib

# import required dependencies
module_checker_lib.check_for_modules(
    ['pandas', 'numpy', 'matplotlib', 'seaborn'])
from pandashells.lib import plot_lib
from pandashells.lib import io_lib
import pylab as pl  # noqa
import seaborn as sns

sns.set_context('talk')


def main():
    msg = textwrap.dedent(
        """
        Creates faceted plots using seaborn FacetGrid.

        With this tool, you can create a group of plots which show aspects
        of the same dataset broken down in different ways.  See the seaborn
        FacetGrid documentation for more detail.

        The --map argument to this function specifies a function to use
        for generating each of the plots.  The following modules are available
        in the namespace:
            pl = pylab
            sns = seaborn
        -----------------------------------------------------------------------
        Examples:

            * Scatterplot of tips vs bill for different combinations of sex,
              smoker, and day of the week:
                    p.example_data -d tips | \\
                    p.facet_grid --row smoker --col sex --hue day \\
                    --map pl.scatter \\
                    --args total_bill tip --kwargs 'alpha=.2' 's=100'

            * Histogram of tips broken down by sex, smoker and day
                    p.example_data -d tips | p.facet_grid --col day \\
                    --row sex --hue smoker  --sharex --sharey --aspect 1 \\
                    --map pl.hist --args tip \\
                    --kwargs 'alpha=.2' 'range=[0, 10]' 'bins=20'
        -----------------------------------------------------------------------
        """
    )

    #  read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    arg_lib.add_args(parser, 'io_in')

    msg = 'Different values of this variable in separate rows'
    parser.add_argument(
        '--row', nargs=1, type=str, dest='row', metavar='row', help=msg)

    msg = 'Different values of this variable in separate columns'
    parser.add_argument(
        '--col', nargs=1, type=str, dest='col', metavar='col', help=msg)

    msg = 'Different values of this variable in separate colors'
    parser.add_argument(
        '--hue', nargs=1, type=str, dest='hue', metavar='hue', help=msg)

    msg = 'The aspect ratio of each plot'
    parser.add_argument(
        '--aspect', nargs=1, type=float, dest='aspect', metavar='aspect',
        default=[2], help=msg)

    msg = 'The size of each plot (default=4)'
    parser.add_argument(
        '--size', nargs=1, type=float, dest='size', metavar='size',
        help=msg, default=[4])

    msg = 'The plotting function to use for each facet'
    parser.add_argument(
        '--map', nargs=1, type=str, dest='map', metavar='map', required=True,
        help=msg)

    msg = 'The args to pass to the plotting function'
    parser.add_argument(
        '--args', nargs='+', type=str, dest='args', metavar='args',
        required=True, help=msg)

    msg = 'Plotting function kwargs expressed as \'a=1\' \'b=2\' ... '
    parser.add_argument(
        '--kwargs', nargs='+', type=str, dest='kwargs',
        metavar='kwargs', help=msg)

    msg = 'Share x axis'
    parser.add_argument('--sharex', action='store_true', dest='sharex',
                        default=False, help=msg)

    msg = 'Share y axis'
    parser.add_argument('--sharey', action='store_true', dest='sharey',
                        default=False, help=msg)

    msg = 'x axis limits when sharex=True'
    parser.add_argument(
        '--xlim', nargs=2, type=float, dest='xlim', metavar='xlim', help=msg)

    msg = 'y axis limits when sharex=True'
    parser.add_argument(
        '--ylim', nargs=2, type=float, dest='ylim', metavar='ylim', help=msg)

    msg = "Save the figure to this file"
    parser.add_argument('--savefig', nargs=1, type=str, help=msg)

    warnings.filterwarnings('ignore')
    # parse arguments
    args = parser.parse_args()

    # get the input dataframe
    df = io_lib.df_from_input(args)

    facet_grid_kwargs = {
        'row': args.row[0] if args.row else None,
        'col': args.col[0] if args.col else None,
        'hue': args.hue[0] if args.hue else None,
        'aspect': args.aspect[0],
        'height': args.size[0],
        'sharex': args.sharex,
        'sharey': args.sharey,
        'xlim': args.xlim if args.xlim else None,
        'ylim': args.ylim if args.ylim else None,
    }
    grid = sns.FacetGrid(df, **facet_grid_kwargs)

    map_func_name = args.map[0]

    scope = {'pl': pl, 'sns': sns, 'map_func_name': map_func_name}
    exec('map_func = {}'.format(map_func_name), scope)
    map_func = scope['map_func']

    map_args = args.args

    map_kwargs = {}
    if args.kwargs:
        for kwarg in args.kwargs:
            exec('map_kwargs.update(dict({}))'.format(kwarg))

    grid.map(map_func, *map_args, **map_kwargs)  # noqa  defined in exec above
    grid.add_legend()
    plot_lib.show(args)


if __name__ == '__main__':  # pragma: no cover
    main()
