#! /usr/bin/env python
import sys
import numpy as np
import pandas as pd
from unittest import TestCase
from pandashells.lib import io_lib
from mock import patch, MagicMock
try:
    from StringIO import StringIO
except ImportError:  # pragma nocover
    from io import StringIO


class IOLibTests(TestCase):
    def test_get_separator_csv(self):
        config_dict = {'io_input_type': 'csv'}
        args = MagicMock(input_options=['csv'])
        self.assertEqual(',', io_lib.get_separator(args, config_dict))

    def test_get_separator_table(self):
        config_dict = {'io_input_type': 'csv'}
        args = MagicMock(input_options=['table'])
        self.assertEqual(r'\s+', io_lib.get_separator(args, config_dict))

    def test_get_separator_default(self):
        config_dict = {'io_input_type': 'csv'}
        args = MagicMock(input_options=[])
        self.assertEqual(',', io_lib.get_separator(args, config_dict))

    def test_get_header_names_with_names_and_header(self):
        args = MagicMock(names=['a'], input_options=[])
        header, names = io_lib.get_header_names(args)
        self.assertEqual(header, 0)
        self.assertEqual(names, ['a'])

    def test_get_header_names_with_names_and_no_header(self):
        args = MagicMock(names=['a'], input_options=['noheader'])
        header, names = io_lib.get_header_names(args)
        self.assertEqual(header, None)
        self.assertEqual(names, ['a'])

    def test_get_header_names_with_no_names_and_header(self):
        args = MagicMock(names=None, input_options=[])
        header, names = io_lib.get_header_names(args)
        self.assertEqual(header, 'infer')
        self.assertEqual(names, None)

    def test_get_header_names_with_no_names_and_no_header(self):
        args = MagicMock(names=None, input_options=['noheader'])
        header, names = io_lib.get_header_names(args)
        self.assertEqual(header, None)
        self.assertEqual(names, None)

    def test_get_nan_rep_with_nan(self):
        config_dict = {'io_output_na_rep': '-'}
        args = MagicMock(io_output_na_rep=['-'])
        self.assertEqual(io_lib.get_nan_rep(args, config_dict), '-')

    def test_get_nan_rep_no_arg(self):
        config_dict = {'io_output_na_rep': 'nan'}
        args = MagicMock(io_output_na_rep=None)
        self.assertTrue(np.isnan(io_lib.get_nan_rep(args, config_dict)))

    @patch('pandashells.lib.io_lib.sys.stdin')
    @patch('pandashells.lib.io_lib.pd')
    def test_df_from_input_no_infile(self, pd_mock, stdin_mock):
        pd_mock.read_csv = MagicMock(return_value=pd.DataFrame())
        args = MagicMock(names=[], input_options=[])
        io_lib.df_from_input(args, in_file=None)
        self.assertEqual(pd_mock.read_csv.call_args_list[0][0][0], stdin_mock)

    @patch('pandashells.lib.io_lib.pd')
    def test_df_from_input_with_infile(self, pd_mock):
        pd_mock.read_csv = MagicMock(return_value=pd.DataFrame())
        args = MagicMock(names=[], input_options=[])
        in_file = MagicMock()
        io_lib.df_from_input(args, in_file=in_file)
        self.assertEqual(pd_mock.read_csv.call_args_list[0][0][0], in_file)

    @patch('pandashells.lib.io_lib.pd')
    def test_df_from_input_tsv(self, pd_mock):
        pd_mock.read_csv = MagicMock(return_value=pd.DataFrame())
        args = MagicMock(names=[], input_options=['tsv'])
        in_file = MagicMock()
        io_lib.df_from_input(args, in_file=in_file)
        self.assertEqual(pd_mock.read_csv.call_args_list[0][0][0], in_file)

    @patch('pandashells.lib.io_lib.json')
    @patch('pandashells.lib.io_lib.open_file')
    def test_df_from_input_json_bad(self, open_file, json):
        open_file.return_value = MagicMock()
        json.loads = MagicMock()
        json.loads.side_effect = ValueError()
        args = MagicMock(names=[], input_options=['json'])
        in_file = MagicMock()
        with self.assertRaises(SystemExit):
            io_lib.df_from_input(args, in_file=in_file)

    @patch('pandashells.lib.io_lib.json')
    @patch('pandashells.lib.io_lib.open_file')
    def test_df_from_input_json(self, open_file, json):
        open_file.return_value = MagicMock()
        json.loads = MagicMock(return_value=[{'a': 1}, {'a': 2}])
        args = MagicMock(names=[], input_options=['json'])
        in_file = MagicMock()
        df = io_lib.df_from_input(args, in_file=in_file)
        self.assertEqual(list(df.columns), ['a'])
        self.assertEqual(list(df.a), [1, 2])

    @patch('pandashells.lib.io_lib.json')
    @patch('pandashells.lib.io_lib.open_file')
    def test_df_from_input_json_names(self, open_file, json):
        open_file.return_value = MagicMock()
        json.loads = MagicMock(return_value=[{'a': 1}, {'a': 2}])
        args = MagicMock(names=['a'], input_options=['json'])
        in_file = MagicMock()
        df = io_lib.df_from_input(args, in_file=in_file)
        self.assertEqual(list(df.columns), ['a'])
        self.assertEqual(list(df.a), [1, 2])

    @patch('pandashells.lib.io_lib.pd')
    def test_df_from_input_no_input(self, pd_mock):
        def raiser(*args, **kwargs):
            raise ValueError()
        pd_mock.read_csv = raiser
        args = MagicMock(names=[], input_options=[])
        in_file = MagicMock()
        with self.assertRaises(SystemExit):
            io_lib.df_from_input(args, in_file=in_file)

    @patch('pandashells.lib.io_lib.pd')
    def test_df_from_input_create_names(self, pd_mock):
        df_in = pd.DataFrame(columns=[1, 2])
        pd_mock.read_csv = MagicMock(return_value=df_in)
        pd_mock.Index = pd.Index
        args = MagicMock(names=[], input_options=['noheader'])
        df = io_lib.df_from_input(args, in_file=None)
        self.assertEqual(['c0', 'c1'], list(df.columns))

    @patch('pandashells.lib.io_lib.sys')
    def test_csv_writer(self, sys_mock):
        sys_mock.stdout = StringIO()
        df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'], index=[0, 1])
        io_lib.csv_writer(df, header=True, index=False, na_rep='nan')
        sys.stdout = sys.__stdout__
        self.assertEqual('"a","b"\n1,2\n3,4\n', sys_mock.stdout.getvalue())

    @patch('pandashells.lib.io_lib.sys')
    def test_table_writer(self, sys_mock):
        sys_mock.stdout = StringIO()
        df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'], index=[0, 1])
        io_lib.table_writer(df, header=True, index=False, na_rep='nan')
        sys.stdout = sys.__stdout__
        self.assertEqual(' a  b\n 1  2\n 3  4\n', sys_mock.stdout.getvalue())

    @patch('pandashells.lib.io_lib.sys')
    def test_html_writer(self, sys_mock):
        sys_mock.stdout = StringIO()
        df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'], index=[0, 1])
        io_lib.html_writer(df, header=True, index=False, na_rep='nan')
        sys.stdout = sys.__stdout__
        html = sys_mock.stdout.getvalue()
        self.assertTrue('<th>a</th>' in html)
        self.assertTrue('<th>b</th>' in html)
        self.assertTrue('<td>1</td>' in html)

    @patch('pandashells.lib.io_lib.sys')
    def test_json_writer(self, sys_mock):
        sys_mock.stdout = StringIO()
        df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'], index=[0, 1])
        io_lib.json_writer(df, header=True, index=False)
        sys.stdout = sys.__stdout__
        json = sys_mock.stdout.getvalue()
        self.assertTrue('"a":1,' in json)

    @patch('pandashells.lib.io_lib.get_nan_rep', MagicMock(return_value='nan'))
    @patch('pandashells.lib.io_lib.csv_writer')
    def test_df_to_output_no_header_no_index(self, csv_writer_mock):
        args_mock = MagicMock(output_options=['csv', 'noheader'])
        df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'], index=[0, 1])
        io_lib.df_to_output(args_mock, df)
        csv_writer_mock.assert_called_with(df, False, False, 'nan')

    @patch('pandashells.lib.io_lib.get_nan_rep', MagicMock(return_value='nan'))
    @patch('pandashells.lib.io_lib.csv_writer')
    def test_df_to_output_csv_type(self, csv_writer_mock):
        args_mock = MagicMock(output_options=['csv', 'index'])
        df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'], index=[0, 1])
        io_lib.df_to_output(args_mock, df)
        csv_writer_mock.assert_called_with(df, True, True, 'nan')

    @patch('pandashells.lib.io_lib.get_nan_rep', MagicMock(return_value='nan'))
    @patch('pandashells.lib.io_lib.csv_writer')
    def test_df_to_output_bad_type(self, csv_writer_mock):
        args_mock = MagicMock(output_options=['bad'])
        df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'], index=[0, 1])
        io_lib.df_to_output(args_mock, df)
        csv_writer_mock.assert_called_with(df, True, False, 'nan')

    @patch('pandashells.lib.io_lib.sys')
    def test_df_to_output_broken_stdout(self, sys_mock):
        args_mock = MagicMock(output_options=['table'])
        df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'], index=[0, 1])
        sys_mock.stdout.write = MagicMock(side_effect=IOError)

        io_lib.df_to_output(args_mock, df)
        self.assertTrue(sys_mock.stdout.write.called)
