#! /usr/bin/env python

import argparse
import textwrap

from pandashells.lib import module_checker_lib
module_checker_lib.check_for_modules(['pandas', 'matplotlib'])

from pandashells.lib import arg_lib, io_lib, plot_lib


def main():
    msg = textwrap.dedent(
        """
        Creates interactive xy plots.  Loosely based around matplotlib's
        pyplot.plot command.

        -----------------------------------------------------------------------
        Examples:

            * Really simple plot
                p.linspace 1 10 7 | p.plot -x c0 -y c0

            * Plot two traces
                p.linspace 0 6.28 100\\
                | p.df 'df["cos"]=np.cos(df.t)' 'df["sin"]=np.sin(df.t)'\\
                        --names t\\
                | p.plot -x t -y sin cos\\
                         --style '.-' 'o-' --alpha 1 .2 --legend best

            * Plot sea-level time series
                p.example_data -d sealevel\\
                | p.plot -x year -y sealevel_mm --style '.'\\
                --xlabel year --ylabel 'relative sea level (mm)'\\
                --title 'Sea Level Rise' --legend best --xlim 1995 2015
        -----------------------------------------------------------------------
        """
    )

    #  read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    arg_lib.add_args(parser, 'io_in', 'xy_plotting', 'decorating')

    parser.add_argument(
        "-a", "--alpha", help="Set opacity level(s)", nargs='+', default=[1.],
        type=float, metavar='alpha')

    # parse arguments
    args = parser.parse_args()

    # get the input dataframe
    df = io_lib.df_from_input(args)

    # set the appropriate theme
    plot_lib.set_plot_styling(args)

    # draw the plot
    plot_lib.draw_xy_plot(args, df)


if __name__ == '__main__':  # pragma: nocover
    main()
