#! /usr/bin/env python


from mock import patch
from unittest import TestCase
import pandas as pd
import pylab as pl

from pandashells.bin.p_scatter_matrix import main


class MainTests(TestCase):
    @patch(
        'pandashells.bin.p_scatter_matrix.sys.argv',
        'p.scatter_matrix'.split())
    @patch('pandashells.bin.p_scatter_matrix.io_lib.df_from_input')
    @patch('pandashells.bin.p_scatter_matrix.plot_lib.show')
    def test_no_spec_cols(self, show_mock, input_mock):
        df_in = pd.DataFrame([
            {'a': 1, 'b': 10, 'c': 100},
            {'a': 2, 'b': 20, 'c': 200},
            {'a': 3, 'b': 30, 'c': 300},
            {'a': 4, 'b': 40, 'c': 400},
        ])
        input_mock.return_value = df_in
        main()
        self.assertEqual(len(pl.gcf().axes), 9)
        self.assertTrue(show_mock.called)

    @patch(
        'pandashells.bin.p_scatter_matrix.sys.argv',
        'p.scatter_matrix -c a b'.split())
    @patch('pandashells.bin.p_scatter_matrix.io_lib.df_from_input')
    @patch('pandashells.bin.p_scatter_matrix.plot_lib.show')
    def test_spec_cols(self, show_mock, input_mock):
        df_in = pd.DataFrame([
            {'a': 1, 'b': 10, 'c': 100},
            {'a': 2, 'b': 20, 'c': 200},
            {'a': 3, 'b': 30, 'c': 300},
            {'a': 4, 'b': 40, 'c': 400},
        ])
        input_mock.return_value = df_in
        main()
        self.assertEqual(len(pl.gcf().axes), 4)
        self.assertTrue(show_mock.called)

    @patch(
        'pandashells.bin.p_scatter_matrix.sys.argv',
        'p.scatter_matrix -c bad b'.split())
    @patch('pandashells.bin.p_scatter_matrix.io_lib.df_from_input')
    @patch('pandashells.bin.p_scatter_matrix.plot_lib.show')
    def test_bad_cols(self, show_mock, input_mock):
        df_in = pd.DataFrame([
            {'a': 1, 'b': 10, 'c': 100},
            {'a': 2, 'b': 20, 'c': 200},
            {'a': 3, 'b': 30, 'c': 300},
            {'a': 4, 'b': 40, 'c': 400},
        ])
        input_mock.return_value = df_in
        with self.assertRaises(ValueError):
            main()
