#! /usr/bin/env python
import argparse
import json
import os


from mock import patch, MagicMock, call
from unittest import TestCase
import pandas as pd

from pandashells.lib import arg_lib, config_lib
from pandashells.bin.p_df import (
    needs_plots,
    get_modules_and_shortcuts,
    framify,
)


class NeedsPlots(TestCase):
    def test_doesnt_need_plots(self):
        command_list = ['df.reset_index()', 'df.head()']
        self.assertFalse(needs_plots(command_list))
    def test_needs_plots(self):
        command_list = ['set_xlim([1, 2])']
        self.assertTrue(needs_plots(command_list))


class GetModulesAndShortcutsTests(TestCase):
    def test_no_extra_needed(self):
        command_list = ['df.reset_index()', 'df.head()']
        self.assertEqual(
            set(get_modules_and_shortcuts(command_list)),
            {
                ('pandas', 'pd'),
                ('dateutil', 'dateutil'),
            }
        )

    def test_get_extra_import_all_needed(self):
        command_list = [
            'pl.plot(df.x)',
            'sns.distplot(df.x)',
            'scp.stats.norm(1, 1)',
            'np.random.randn(1)'
        ]
        self.assertEqual(
            set(get_modules_and_shortcuts(command_list)),
            {
                ('dateutil', 'dateutil'),
                ('pandas', 'pd'),
                ('scipy', 'scp'),
                ('pylab', 'pl'),
                ('seaborn', 'sns'),
                ('numpy', 'np'),
            },
        )

class FramifyTests(TestCase):
    def test_dataframe_to_dataframe(self):
        cmd = ''
        df = pd.DataFrame([{'a': 1}])
        out = framify(cmd, df)
        self.assertTrue(isinstance(out), pd.DataFrame)

    def test_series_to_dataframe(self):
        cmd = ''
        df = pd.Series({'a': 1})
        out = framify(cmd, df)
        self.assertTrue(isinstance(out), pd.DataFrame)

    def test_list_to_dataframe(self):
        cmd = ''
        df = [1, 2, 3]
        out = framify(cmd, df)
        self.assertTrue(isinstance(out), pd.DataFrame)

    @patch('pandashells.bin.p_df.sys.stderr.write')
    @patch('pandashells.bin.p_df.sys.exit')
    def test_list_to_dataframe(self, exit_mock, write_mock):
        cmd = ''
        df = 7
        out = framify(cmd, df)
        assert that exit was called here

