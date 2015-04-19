#! /usr/bin/env python

import argparse

from pandashells.lib import module_checker_lib, arg_lib, io_lib, plot_lib

module_checker_lib.check_for_modules(['pandas', 'matplotlib'])


def main():
    #TODO: Finish this help message
    msg = "Write "
    msg += "something here"

    # read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    arg_lib.add_args(parser, 'io_in', 'xy_plotting', 'decorating', 'example')

    parser.add_argument(
        "-a", "--alpha", help="Set opacity", nargs=1, default=[1.], type=float)

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
