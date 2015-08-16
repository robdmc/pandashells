#! /usr/bin/env python
import subprocess

from mock import patch, MagicMock
from unittest import TestCase
import pandas as pd
import numpy as np

try:
    from StringIO import StringIO
except ImportError:  # pragma nocover
    from io import StringIO

from pandashells.bin.p_sig_edit import (
    main,
)


class MainUnitTest(TestCase):
    @patch('pandashells.bin.p_sig_edit.io_lib')
    @patch('pandashells.bin.p_sig_edit.outlier_lib.sigma_edit_dataframe')
    @patch('pandashells.bin.p_sig_edit.argparse.ArgumentParser')
    def test_from_input_to_output(
            self, arg_parser_mock, sig_edit_mock, io_lib_mock):
        df_in = pd.DataFrame([
            {'a': 1, 'b': 10},
            {'a': 2, 'b': 20},
            {'a': 3, 'b': 30},
            {'a': 4, 'b': 40},
        ])

        args = MagicMock()
        args.sigma_thresh = [3.]
        args.cols = ['a']
        args.max_iter = [20]

        parser = MagicMock(parse_args=MagicMock(return_value=args))
        arg_parser_mock.return_value = parser
        arg_parser_mock.parse_args = args
        io_lib_mock.df_to_output = MagicMock()
        io_lib_mock.df_from_input = MagicMock(return_value=df_in)
        main()
        sig_edit_mock.assert_called_with(3., ['a'], df_in, max_iter=20)
        self.assertTrue(io_lib_mock.df_to_output.called)


class IntegrationTests(TestCase):
    def setUp(self):
        self.df = pd.DataFrame([
            {'a': 1},
            {'a': 2},
            {'a': 1},
            {'a': 2},
            {'a': 1},
            {'a': 2},
            {'a': 1},
            {'a': 2},
            {'a': 6},
        ])

    def get_command_result(self, cmd):
        p = subprocess.Popen(
            ['bash', '-c', cmd],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = p.communicate(
            self.df.to_csv(index=False).encode('utf-8'))
        return stdout.decode('utf-8').strip()

    def test_editing(self):
        cmd = 'p.sig_edit -t 2 -c a'
        df = pd.read_csv(StringIO(self.get_command_result(cmd)))
        self.assertTrue(np.isnan(df.a.iloc[-1]))
        self.assertEqual(len(df.dropna()), 8)

    def test_bad_iter(self):
        cmd = 'p.sig_edit -t 2 -c a --max_iter 0'
        with self.assertRaises(ValueError):
            pd.read_csv(StringIO(self.get_command_result(cmd)))
