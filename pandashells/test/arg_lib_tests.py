#! /usr/bin/env python
import os
import json
from unittest import TestCase
from pandashells.lib import arg_lib, config_lib
import argparse
from mock import patch, MagicMock, call


class ArgLibTests(TestCase):
    def setUp(self):
        pass

    def test_check_for_recognized_args_bad_args(self):
        """
        _check_for_recognized_args properly recognizes bad arguments
        """
        with self.assertRaises(ValueError):
            arg_lib._check_for_recognized_args('unrecognized', 'args')

    def test_check_for_recognized_args_good_args(self):
        """
        _check_for_recognized_args properly accepts good args
        """
        args = [
            'io_in',
            'io_out',
            'example',
            'xy_plotting',
            'decorating',
        ]
        arg_lib._check_for_recognized_args(*args)

    def test_io_in_adder_inactive(self):
        """
        _io_in_adder doesn't do anything when io_in not specified
        """
        parser = MagicMock()
        parser.add_argument = MagicMock()
        args = []
        arg_lib._io_in_adder(parser, {}, *args)
        self.assertFalse(parser.add_argument.called)

    def test_io_in_adder_active(self):
        """
        _io_in_adder adds proper arguments
        """
        # --- set up mock parser
        parser = MagicMock()
        parser.add_argument = MagicMock()

        # --- create a list of expected call signatures
        calls = []
        msg = 'Overwrite column names with list of names'
        calls.append(
            call('--names', nargs='+', type=str, dest='names', metavar="name",
            help=msg)
        )

        default_for_input = ['csv', 'header']
        io_opt_list = ['csv', 'table', 'header', 'noheader']
        calls.append(call('-i', '--input_options', nargs='+',
            type=str, dest='input_options', metavar='option',
            default=default_for_input, choices=io_opt_list,
            help='Input Options')
        )

        # --- run the code under test
        args = ['io_in']
        config_dict = {'io_input_type': 'csv', 'io_input_header': 'header'}
        arg_lib._io_in_adder(parser, config_dict, *args)

        # --- make sure proper calls were made
        self.assertEqual(parser.add_argument.call_args_list, calls)

    def test_io_out_adder_inactive(self):
        """
        _io_out_adder doesn't do anything when io_out not specified
        """
        parser = MagicMock()
        parser.add_argument = MagicMock()
        args = []
        arg_lib._io_out_adder(parser, {}, *args)
        self.assertFalse(parser.add_argument.called)

    def test_io_out_adder_active(self):
        """
        _io_out_adder adds proper arguments
        """
        # --- set up mock parser
        parser = MagicMock()
        parser.add_argument = MagicMock()

        # --- create  expected call signature
        io_opt_list = ['csv', 'table', 'html',
                       'header', 'noheader', 'index', 'noindex']
        # --- define the current defaults
        default_for_output = ['csv', 'header', 'noindex']
        msg = 'Options taken from {}'.format(repr(io_opt_list))
        call_obj = call('-o', '--output_options', nargs='+',
                            type=str, dest='output_options', metavar='option',
                            default=default_for_output, help=msg)

        # --- run the code under test
        args = ['io_out']
        config_dict = {
            'io_output_type': 'csv',
            'io_output_header': 'header',
            'io_output_index': 'index'
        }
        arg_lib._io_out_adder(parser, config_dict, *args)

        # --- make sure proper calls were made
        parser.add_argument.assertCalledWith(call_obj)

    def test_decorating_adder_inactive(self):
        """
        _decorating_adder doesn't do anything when decorating not specified
        """
        parser = MagicMock()
        parser.add_argument = MagicMock()
        args = []
        arg_lib._decorating_adder(parser, *args)
        self.assertFalse(parser.add_argument.called)

    def test_decorating_adder_active(self):
        """
        _decorating_adder adds proper arguments
        """
        # --- set up mock parser
        parser = MagicMock()
        parser.add_argument = MagicMock()

        # --- create a list of expected call signatures
        calls = []

        context_list = [t for t in config_lib.CONFIG_OPTS if
                        t[0] == 'plot_context'][0][1]
        theme_list = [t for t in config_lib.CONFIG_OPTS if
                      t[0] == 'plot_theme'][0][1]
        palette_list = [t for t in config_lib.CONFIG_OPTS if
                        t[0] == 'plot_palette'][0][1]

        msg = "Set the x-limits for the plot"
        calls.append(call('--xlim', nargs=2, type=float, dest='xlim',
                          metavar=('XMIN', 'XMAX'), help=msg))

        msg = "Set the y-limits for the plot"
        calls.append(call('--ylim', nargs=2, type=float, dest='ylim',
                          metavar=('YMIN', 'YMAX'), help=msg))

        msg = "Set the x-label for the plot"
        calls.append(call('--xlabel', nargs=1, type=str, dest='xlabel',
                          help=msg))

        msg = "Set the y-label for the plot"
        calls.append(call('--ylabel', nargs=1, type=str, dest='ylabel',
                          help=msg))

        msg = "Set the title for the plot"
        calls.append(call('--title', nargs=1, type=str, dest='title', help=msg))


        msg = "Specify legend location"
        calls.append(call('--legend', nargs=1, type=str, dest='legend',
                          choices=['1', '2', '3', '4', 'best'], help=msg))

        msg = "Specify whether hide the grid or not"
        calls.append(call('--nogrid',  action='store_true', dest='no_grid',
                          default=False,  help=msg))


        msg = "Specify plot context. Default = '{}' ".format(context_list[0])
        calls.append(call('--context', nargs=1, type=str, dest='plot_context',
                          default=[context_list[0]], choices=context_list,
                          help=msg))

        msg = "Specify plot theme. Default = '{}' ".format(theme_list[0])
        calls.append(call('--theme', nargs=1,
                          type=str, dest='plot_theme', default=[theme_list[0]],
                          choices=theme_list, help=msg))

        msg = "Specify plot palette. Default = '{}' ".format(palette_list[0])
        calls.append(call('--palette', nargs=1, type=str, dest='plot_palette',
                          default=[palette_list[0]], choices=palette_list,
                          help=msg))

        msg = "Save the figure to this file"
        calls.append(call('--savefig', nargs=1, type=str, help=msg))

        # --- run the code under test
        args = ['decorating']
        arg_lib._decorating_adder(parser, *args)

        # --- make sure proper calls were made
        self.assertEqual(parser.add_argument.call_args_list, calls)
