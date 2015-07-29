#! /usr/bin/env python


from mock import patch
from unittest import TestCase
import pandas as pd

from pandashells.bin.p_facet_grid import main


class MainTests(TestCase):
    @patch(
        'pandashells.bin.p_facet_grid.sys.argv',
        'p.facet_grid --row c --map pl.plot --args a b'.split())
    @patch('pandashells.bin.p_facet_grid.io_lib.df_from_input')
    @patch('pandashells.bin.p_facet_grid.plot_lib.show')
    def test_no_kwargs(self, show_mock, input_mock):
        import pylab as pl
        df_in = pd.DataFrame([
            {'a': 1, 'b': 10, 'c': 'alpha'},
            {'a': 2, 'b': 20, 'c': 'alpha'},
            {'a': 3, 'b': 30, 'c': 'beta'},
            {'a': 4, 'b': 40, 'c': 'beta'},
        ])
        input_mock.return_value = df_in
        main()
        self.assertEqual(len(pl.gcf().axes), 2)
        self.assertTrue(show_mock.called)

    @patch(
        'pandashells.bin.p_facet_grid.sys.argv',
        (
            'p.facet_grid --row c --map pl.scatter '
            '--args a b --kwargs s=100'.split()
        )
    )
    @patch('pandashells.bin.p_facet_grid.io_lib.df_from_input')
    @patch('pandashells.bin.p_facet_grid.plot_lib.show')
    def test_with_kwargs(self, show_mock, input_mock):
        import pylab as pl
        df_in = pd.DataFrame([
            {'a': 1, 'b': 10, 'c': 'alpha'},
            {'a': 2, 'b': 20, 'c': 'alpha'},
            {'a': 3, 'b': 30, 'c': 'beta'},
            {'a': 4, 'b': 40, 'c': 'beta'},
        ])
        input_mock.return_value = df_in
        main()
        self.assertEqual(len(pl.gcf().axes), 2)
        self.assertTrue(show_mock.called)
