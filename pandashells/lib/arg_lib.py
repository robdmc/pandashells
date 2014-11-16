import os
import sys
import inspect

from pandashells.lib import config_lib


def _check_for_recognized_args(*args):
    """
    Raise an error if unrecognized argset is specified
    """
    allowed_arg_set = set([
        'io_in',
        'io_out',
        'example',
        'xy_plotting',
        'decorating',
    ])

    in_arg_set = set(args)
    unrecognized_set = in_arg_set - allowed_arg_set
    if unrecognized_set:
        msg = '{} not in allowed set {}'.format(unrecognized_set,
                                                allowed_arg_set)
        raise ValueError(msg)


def _io_in_adder(parser, config_dict, *args):
    """
    Add input options to the parser
    """
    in_arg_set = set(args)
    if 'io_in' in in_arg_set:
        # --- define the valid components
        io_opt_list = ['csv', 'table', 'header', 'noheader']

        # --- allow the option of supplying input column names
        msg = 'Overwrite column names with list of names'
        parser.add_argument('--names', nargs='+', type=str,
                            dest='names', metavar="name",
                            help=msg)

        default_for_input = [config_dict['io_input_type'],
                             config_dict['io_input_header']]

        parser.add_argument('-i', '--input_options', nargs='+',
                            type=str, dest='input_options', metavar='option',
                            default=default_for_input, choices=io_opt_list,
                            help='Input Options')


def _io_out_adder(parser, config_dict, *args):
    """
    Add output options to the parser
    """
    in_arg_set = set(args)
    if 'io_out' in in_arg_set:
        # --- define the valid components
        io_opt_list = ['csv', 'table', 'html',
                       'header', 'noheader', 'index', 'noindex']

        # --- define the current defaults
        default_for_output = [config_dict['io_output_type'],
                              config_dict['io_output_header'],
                              config_dict['io_output_index']]

        # --- show the current defaults in the arg parser
        msg = 'Options taken from {}'.format(repr(io_opt_list))
        parser.add_argument('-o', '--output_options', nargs='+',
                            type=str, dest='output_options', metavar='option',
                            default=default_for_output, help=msg)


def _decorating_adder(parser, *args):
    in_arg_set = set(args)
    if 'decorating' in in_arg_set:
        # --- get a list of valid plot styling info
        context_list = [t for t in config_lib.CONFIG_OPTS if
                        t[0] == 'plot_context'][0][1]
        theme_list = [t for t in config_lib.CONFIG_OPTS if
                      t[0] == 'plot_theme'][0][1]
        palette_list = [t for t in config_lib.CONFIG_OPTS if
                        t[0] == 'plot_palette'][0][1]

        # ---
        msg = "Set the x-limits for the plot"
        parser.add_argument('--xlim', nargs=2, type=float, dest='xlim',
                            metavar=('XMIN', 'XMAX'), help=msg)
        # ---
        msg = "Set the y-limits for the plot"
        parser.add_argument('--ylim', nargs=2, type=float, dest='ylim',
                            metavar=('YMIN', 'YMAX'), help=msg)
        # ---
        msg = "Set the x-label for the plot"
        parser.add_argument('--xlabel', nargs=1, type=str, dest='xlabel',
                            help=msg)
        # ---
        msg = "Set the y-label for the plot"
        parser.add_argument('--ylabel', nargs=1, type=str, dest='ylabel',
                            help=msg)
        # ---
        msg = "Set the title for the plot"
        parser.add_argument('--title', nargs=1, type=str, dest='title',
                            help=msg)
        # ---
        msg = "Specify legend location"
        parser.add_argument('--legend', nargs=1, type=str, dest='legend',
                            choices=['1', '2', '3', '4', 'best'], help=msg)
        # ---
        msg = "Specify whether hide the grid or not"
        parser.add_argument('--nogrid',  action='store_true', dest='no_grid',
                            default=False,  help=msg)

        # ---
        msg = "Specify plot context. Default = '{}' ".format(context_list[0])
        parser.add_argument('--context', nargs=1,
                            type=str, dest='plot_context',
                            default=[context_list[0]], choices=context_list,
                            help=msg)
        # ---
        msg = "Specify plot theme. Default = '{}' ".format(theme_list[0])
        parser.add_argument('--theme', nargs=1,
                            type=str, dest='plot_theme',
                            default=[theme_list[0]], choices=theme_list,
                            help=msg)
        # ---
        msg = "Specify plot palette. Default = '{}' ".format(palette_list[0])
        parser.add_argument('--palette', nargs=1,
                            type=str, dest='plot_palette',
                            default=[palette_list[0]], choices=palette_list,
                            help=msg)
        # ---
        msg = "Save the figure to this file"
        parser.add_argument('--savefig', nargs=1, type=str,
                            help=msg)


def _xy_adder(parser, *args):
    in_arg_set = set(args)
    if 'xy_plotting' in in_arg_set:

        msg = 'Column to plot on x-axis'
        parser.add_argument('-x', nargs=1, type=str, dest='x', metavar='col',
                            help=msg)

        msg = 'List of columns to plot on y-axis'
        parser.add_argument('-y', nargs='+', type=str, dest='y',
                            metavar='col', help=msg)

        msg = "Plot style defaults to .-"
        parser.add_argument('-s', '--style', nargs=1, type=str, dest='style',
                            default=['.-'], help=msg)


def _example_adder(parser, *args):
    in_arg_set = set(args)
    if 'example' in in_arg_set:
        msg = "Show a usage example and exit"
        parser.add_argument('--example', action='store_true', dest='example',
                            default=False,  help=msg)


def add_args(parser, *args):
    """Adds argument blocks to the arg parser

    :type parser: argparse instance
    :param parser: The argarse instance to use in adding arguments

    Additinional arguments are the names of argument blocks to add
    """
    config_dict = config_lib.get_config()
    _check_for_recognized_args(*args)
    _io_in_adder(parser, config_dict, *args)
    _io_out_adder(parser, config_dict, *args)
    _decorating_adder(parser, *args)
    _xy_adder(parser, *args)
    _example_adder(parser, *args)
