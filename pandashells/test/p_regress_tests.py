#! /usr/bin/env python
import sys
import re
from mock import patch, MagicMock
from unittest import TestCase
import numpy as np
import pandas as pd

from pandashells.bin.p_regress import main


class MainTests(TestCase):
    @patch(
        'pandashells.bin.p_regress.sys.argv',
        'p.regress -m y~x'.split())
    @patch('pandashells.bin.p_regress.io_lib.df_to_output')
    @patch('pandashells.bin.p_regress.io_lib.df_from_input')
    def test_cli_stats(self, df_from_input_mock, df_to_output_mock):
        df_in = pd.DataFrame({
            'x': range(1, 101),
            'y': range(1, 101),
        })
        df_from_input_mock.return_value = df_in
        write_mock = MagicMock()
        sys.stdout = MagicMock()
        sys.stdout.write = write_mock
        main()
        sys.stdout = sys.__stdout__
        out_str = write_mock.call_args_list[0][0][0].replace('\n', ' ')
        rex = re.compile(r'.*x\s+1\.0+')
        m = rex.match(out_str)
        self.assertTrue(True if m else False)

    @patch(
        'pandashells.bin.p_regress.sys.argv',
        'p.regress -m y~x --plot'.split())
    @patch('pandashells.bin.p_regress.io_lib.df_from_input')
    @patch('pandashells.bin.p_regress.get_module')
    def test_cli_plots_osx(self, get_module_mock, df_from_input_mock):
        backend_mock = MagicMock(lower=MagicMock(return_value='macosx'))
        mpl_mock = MagicMock(get_backend=MagicMock(return_value=backend_mock))
        show_mock = MagicMock()
        plot_lib_mock = MagicMock(show=show_mock)
        get_module_mock.side_effect = [
            plot_lib_mock,
            mpl_mock,
            MagicMock(return_value=MagicMock()),
            MagicMock(return_value=MagicMock()),
        ]
        df_in = pd.DataFrame({
            'x': range(1, 101),
            'y': range(1, 101),
        })
        df_from_input_mock.return_value = df_in
        sys.stdout = MagicMock()
        main()
        sys.stdout = sys.__stdout__
        self.assertTrue(show_mock.called)

    @patch(
        'pandashells.bin.p_regress.sys.argv',
        'p.regress -m y~x --plot'.split())
    @patch('pandashells.bin.p_regress.io_lib.df_from_input')
    @patch('pandashells.bin.p_regress.get_module')
    def test_cli_plots_tkagg(self, get_module_mock, df_from_input_mock):
        backend_mock = MagicMock()
        backend_mock.lower = MagicMock(return_value='tkagg')
        mpl_mock = MagicMock(get_backend=backend_mock)
        show_mock = MagicMock()
        plot_lib_mock = MagicMock(show=show_mock)
        get_module_mock.side_effect = [
            plot_lib_mock,
            mpl_mock,
            MagicMock(return_value=MagicMock()),
            MagicMock(return_value=MagicMock()),
        ]
        df_in = pd.DataFrame({
            'x': range(1, 101),
            'y': range(1, 101),
        })
        df_from_input_mock.return_value = df_in
        sys.stdout = MagicMock()
        main()
        sys.stdout = sys.__stdout__
        self.assertTrue(show_mock.called)

    @patch(
        'pandashells.bin.p_regress.sys.argv',
        'p.regress -m y~x --fit'.split())
    @patch('pandashells.bin.p_regress.io_lib.df_to_output')
    @patch('pandashells.bin.p_regress.io_lib.df_from_input')
    def test_cli_fit(self, df_from_input_mock, df_to_output_mock):
        df_in = pd.DataFrame({
            'x': range(1, 101),
            'y': range(1, 101),
        })
        df_from_input_mock.return_value = df_in
        main()

        df_out = df_to_output_mock.call_args_list[0][0][1]
        self.assertTrue(np.allclose(df_out.y, df_out.fit_))
        self.assertTrue(np.allclose(df_out.y * 0, df_out.resid_))
