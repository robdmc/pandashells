#! /usr/bin/env python
import os
import json
from unittest import TestCase
from pandashells.lib import arg_lib
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

    def test_io_in_inactive(self):
        """
        _io_in_adder doesn't do anything when io_in not specified
        """
        parser = MagicMock()
        parser.add_argument = MagicMock()
        args = []
        config_dict = {'io_input_type': 'csv', 'io_input_header': 'header'}
        arg_lib._io_in_adder(parser, config_dict, *args)
        self.assertFalse(parser.add_argument.called)

    def test_io_in_active(self):
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

    def test_io_out_inactive(self):
        """
        _io_out_adder doesn't do anything when io_out not specified
        """
        parser = MagicMock()
        parser.add_argument = MagicMock()
        args = []
        config_dict = {'io_input_type': 'csv', 'io_input_header': 'header'}
        arg_lib._io_out_adder(parser, config_dict, *args)
        self.assertFalse(parser.add_argument.called)

    def test_io_out_active(self):
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
        config_dict = {'io_input_type': 'csv', 'io_input_header': 'header'}
        arg_lib._io_in_adder(parser, config_dict, *args)

        # --- make sure proper calls were made
        parser.add_argument.assertCalledWith(call_obj)

