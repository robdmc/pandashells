#! /usr/bin/env python
from mock import patch
from unittest import TestCase

from pandashells.bin.p_linspace import main


class TestMain(TestCase):
    @patch(
        'pandashells.bin.p_linspace.sys.argv',
        'p.linspace 0 100 13'.split())
    @patch('pandashells.bin.p_linspace.io_lib.df_to_output')
    def test_linspace(self, df_to_output_mock):
        main()
        df = df_to_output_mock.call_args_list[0][0][1]
        self.assertEqual(df.c0.iloc[0], 0.)
        self.assertEqual(df.c0.iloc[-1], 100.)
        self.assertEqual(len(df), 13)
