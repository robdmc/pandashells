#! /usr/bin/env python
from mock import patch, MagicMock
from unittest import TestCase
import pandas as pd

from pandashells.bin.p_smooth import main, get_input_args, validate_args


class GetInputArgsTests(TestCase):
    @patch('pandashells.bin.p_smooth.sys.argv', 'p.smooth -x x -y y'.split())
    def test_right_number_of_args(self):
        args = get_input_args()
        self.assertEqual(len(args.__dict__), 6)


class ValidateArgs(TestCase):
    def test_okay(self):
        # passing test means nothing raised
        args = MagicMock(quiet=False)
        cols = ['a']
        df = MagicMock(columns=['a'])
        validate_args(args, cols, df)

    @patch('pandashells.bin.p_smooth.sys.stderr')
    def test_bad_cols(self, stderr_mock):
        # passing test means nothing raised
        args = MagicMock(quiet=False)
        cols = ['b']
        df = MagicMock(columns=['a'])
        with self.assertRaises(SystemExit):
            validate_args(args, cols, df)


class MainTests(TestCase):
    @patch(
        'pandashells.bin.p_smooth.sys.argv',
        'p.smooth -x x -y y'.split())
    @patch('pandashells.bin.p_smooth.io_lib.df_to_output')
    @patch('pandashells.bin.p_smooth.io_lib.df_from_input')
    def test_cli(self, df_from_input_mock, df_to_output_mock):
        df_in = pd.DataFrame({
            'x': range(1, 101),
            'y': range(1, 101),
        })
        df_from_input_mock.return_value = df_in
        main()
        dfout = df_to_output_mock
        self.assertEqual(
            list(dfout.call_args_list[0][0][1].columns), ['x', 'y'])
