#! /usr/bin/env python
from mock import patch
from unittest import TestCase

import numpy as np
import pandas as pd
from pandashells.bin.p_regplot import main, make_label


class MakeLabelTests(TestCase):
    def test_make_label_html(self):
        label = make_label(coeffs=[1, 2, 3], savefig=['test.html'])
        self.assertEqual(label, 'y = (3) + (2) x + (1) x ^ 2')

    def test_make_label_tex(self):
        label = make_label(coeffs=[1, 2], savefig=['test.png'])
        self.assertEqual(label, '$y = (2) + (1) x$')


class MainTests(TestCase):
    @patch(
        'pandashells.bin.p_regplot.sys.argv',
        'p.regplot -x x -y y'.split())
    @patch('pandashells.bin.p_regplot.io_lib.df_from_input')
    @patch('pandashells.bin.p_regplot.plot_lib.show')
    def test_cli_non_plain(self, show_mock, df_from_input_mock):
        df_in = pd.DataFrame({
            'x': np.arange(1, 101),
            'y': np.arange(1, 101) + np.random.randn(100)
        })
        df_from_input_mock.return_value = df_in
        main()
        self.assertTrue(show_mock.called)
