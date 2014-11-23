#! /usr/bin/env python
import os
import json
from unittest import TestCase
from pandashells.lib.module_checker_lib import check_for_modules
from pandashells.lib import io_lib
import argparse
from mock import patch, MagicMock, call

class IOLibTests(TestCase):
    def test_get_separator_csv(self):
        """
        get_separator() recognizes csv
        """
        config_dict = {'io_input_type': 'csv'}
        args = MagicMock(input_options=['csv'])
        self.assertEqual(',', io_lib.get_separator(args, config_dict))

    def test_get_separator_table(self):
        """
        get_separator() recognizes table
        """
        config_dict = {'io_input_type': 'csv'}
        args = MagicMock(input_options=['table'])
        self.assertEqual(r'\s+', io_lib.get_separator(args, config_dict))

    def test_get_separator_default(self):
        """
        get_separator() goes to default for unrecognized
        """
        config_dict = {'io_input_type': 'csv'}
        args = MagicMock(input_options=[])
        self.assertEqual(',', io_lib.get_separator(args, config_dict))

    def test_get_header_names_with_names_and_header(self):
        """
        get_header_names() does right thing for names and header
        """
        args = MagicMock(names=['a'], input_options=[])
        header, names = io_lib.get_header_names(args)
        self.assertEqual(header, 0)
        self.assertEqual(names, ['a'])

    def test_get_header_names_with_names_and_no_header(self):
        """
        get_header_names() does right thing for names and header
        """
        args = MagicMock(names=['a'], input_options=['noheader'])
        header, names = io_lib.get_header_names(args)
        self.assertEqual(header, None)
        self.assertEqual(names, ['a'])

    def test_get_header_names_with_no_names_and_header(self):
        """
        get_header_names() does right thing for names and header
        """
        args = MagicMock(names=None, input_options=[])
        header, names = io_lib.get_header_names(args)
        self.assertEqual(header, 'infer')
        self.assertEqual(names, None )

    def test_get_header_names_with_no_names_and_no_header(self):
        """
        get_header_names() does right thing for names and header
        """
        args = MagicMock(names=None, input_options=['noheader'])
        header, names = io_lib.get_header_names(args)
        self.assertEqual(header, None)
        self.assertEqual(names, None )

