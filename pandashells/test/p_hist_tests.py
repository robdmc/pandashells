#! /usr/bin/env python
from mock import patch, MagicMock
from unittest import TestCase
import pandas as pd

from pandashells.bin.p_hist import main, get_input_args, validate_args


class GetInputArgsTests(TestCase):
    @patch('pandashells.bin.p_hist.sys.argv', 'p.hist -c x -n 30'.split())
    def test_right_number_of_args(self):
        args = get_input_args()
        self.assertEqual(len(args.__dict__), 26)


class ValidateArgs(TestCase):
    def test_okay(self):
        # passing test means nothing raised
        args = MagicMock(quiet=False)
        cols = ['a']
        df = MagicMock(columns=['a'])
        validate_args(args, cols, df)

    @patch('pandashells.bin.p_hist.sys.stderr')
    def test_bad_cols(self, stderr_mock):
        # passing test means nothing raised
        args = MagicMock(quiet=False)
        cols = ['b']
        df = MagicMock(columns=['a'])
        with self.assertRaises(SystemExit):
            validate_args(args, cols, df)

    @patch('pandashells.bin.p_hist.sys.stderr')
    def test_bad_quiet(self, stderr_mock):
        # passing test means nothing raised
        args = MagicMock(quiet=True)
        cols = ['a', 'b']
        df = MagicMock(columns=['a', 'b'])
        with self.assertRaises(SystemExit):
            validate_args(args, cols, df)


class MainTests(TestCase):
    @patch(
        'pandashells.bin.p_hist.sys.argv',
        'p.hist -c x -q -n 10'.split())
    @patch('pandashells.bin.p_hist.io_lib.df_to_output')
    @patch('pandashells.bin.p_hist.io_lib.df_from_input')
    def test_cli_quiet(self, df_from_input_mock, df_to_output_mock):
        df_in = pd.DataFrame({
            'x': range(1, 101)
        })
        df_from_input_mock.return_value = df_in
        main()
        df_out = df_to_output_mock.call_args_list[0][0][1]
        self.assertEqual(set(df_out.columns), {'bins', 'counts'})
        self.assertEqual(set(df_out.counts), {10})

    @patch(
        'pandashells.bin.p_hist.sys.argv',
        'p.hist -c x -n 10'.split())
    @patch('pandashells.bin.p_hist.get_imports')
    @patch('pandashells.bin.p_hist.io_lib.df_from_input')
    def test_cli(self, df_from_input_mock, get_imports_mock):
        show_mock = MagicMock()
        plot_lib_mock = MagicMock(show=show_mock)
        get_imports_mock.return_value = plot_lib_mock
        df_in = pd.DataFrame({
            'x': range(1, 101)
        })
        df_from_input_mock.return_value = df_in
        main()
        self.assertTrue(show_mock.called)
