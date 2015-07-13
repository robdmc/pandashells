#! /usr/bin/env python
from mock import patch
from unittest import TestCase
import pandas as pd

from pandashells.bin.p_cdf import main


class MainTests(TestCase):
    @patch(
        'pandashells.bin.p_cdf.sys.argv',
        'p.cdf -c x -q -n 10'.split())
    @patch('pandashells.bin.p_cdf.io_lib.df_to_output')
    @patch('pandashells.bin.p_cdf.io_lib.df_from_input')
    def test_cli_quiet(self, df_from_input_mock, df_to_output_mock):
        df_in = pd.DataFrame({
            'x': range(1, 101)
        })
        df_from_input_mock.return_value = df_in
        main()
        df_out = df_to_output_mock.call_args_list[0][0][1]
        self.assertEqual(list(df_out.columns), ['x', 'p_less', 'p_greater'])
        self.assertEqual(len(df_out), 10)

    @patch(
        'pandashells.bin.p_cdf.sys.argv',
        'p.cdf -c x -n 10'.split())
    @patch('pandashells.bin.p_cdf.plot_lib.show')
    @patch('pandashells.bin.p_cdf.io_lib.df_from_input')
    def test_cli(self, df_from_input_mock, show_mock):
        df_in = pd.DataFrame({
            'x': range(1, 101)
        })
        df_from_input_mock.return_value = df_in
        main()
        self.assertTrue(show_mock.called)
