#! /usr/bin/env python
from mock import patch
from unittest import TestCase
import pandas as pd
import numpy as np

from pandashells.bin.p_lomb_scargle import main


class MainTests(TestCase):
    @patch(
        'pandashells.bin.p_lomb_scargle.sys.argv',
        'p.lomb_scargle -t t -y y'.split())
    @patch('pandashells.bin.p_lomb_scargle.io_lib.df_to_output')
    @patch('pandashells.bin.p_lomb_scargle.io_lib.df_from_input')
    def test_cli(self, df_from_input_mock, df_to_output_mock):
        t = np.linspace(0, 10, 250)
        y = 7 * np.sin(2 * np.pi * t)
        df_in = pd.DataFrame({'t': t, 'y': y})
        df_from_input_mock.return_value = df_in

        main()
        df = df_to_output_mock.call_args_list[0][0][1]

        max_rec = df[df.amp == df.amp.max()].iloc[0]
        self.assertTrue(all([x > 0 for x in df.period.diff().dropna()]))
        self.assertAlmostEqual(max_rec['amp'], 7, places=0)
        self.assertAlmostEqual(max_rec['power'], 49, places=0)
        self.assertAlmostEqual(max_rec['period'], 1, places=0)
        self.assertAlmostEqual(max_rec['freq'], 1, places=0)
        self.assertEqual(len(df), 512)
