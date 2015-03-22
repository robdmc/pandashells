#! /usr/bin/env python

from mock import patch, MagicMock
from unittest import TestCase
import pandas as pd

from pandashells.bin.p_merge import (
    main,
    validate_args,
)


@patch('pandashells.bin.p_merge.sys.stderr')
class ValidateArgsTests(TestCase):
    def test_no_left(self, stderr_mock):
        args = MagicMock(left_on=None, right_on='test')
        with self.assertRaises(SystemExit):
            validate_args(args)

    def test_no_right(self, stderr_mock):
        args = MagicMock(left_on='test', right_on=None)
        with self.assertRaises(SystemExit):
            validate_args(args)

    def test_no_join(self, stderr_mock):
        args = MagicMock(left_on=None, right_on=None, on=None)
        with self.assertRaises(SystemExit):
            validate_args(args)


class MainTests(TestCase):

    @patch(
        'pandashells.bin.p_merge.sys.argv',
        'p.merge le ri --left_on a b --right_on d e'.split())
    @patch('pandashells.bin.p_merge.io_lib.df_to_output')
    @patch('pandashells.bin.p_merge.io_lib.df_from_input')
    def test_cli(self, df_from_input_mock, df_to_output_mock):
        # make two frames to join
        df_left = pd.DataFrame([
            {'a': 1, 'b': 1, 'c': 10},
            {'a': 1, 'b': 2, 'c': 20},
            {'a': 2, 'b': 1, 'c': 30},
            {'a': 2, 'b': 2, 'c': 40},
        ])
        df_right = pd.DataFrame([
            {'d': 1, 'e': 1, 'f': 50},
            {'d': 1, 'e': 2, 'f': 60},
            {'d': 2, 'e': 1, 'f': 70},
            {'d': 2, 'e': 2, 'f': 80},
        ])
        df_from_input_mock.side_effect = [df_left, df_right]

        # make sure join looks right
        main()
        dfj = df_to_output_mock.call_args_list[0][0][1]
        self.assertEqual(list(dfj.c), [10, 20, 30, 40])
        self.assertEqual(list(dfj.f), [50, 60, 70, 80])
