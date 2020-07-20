#! /usr/bin/env python
import os
import subprocess
import tempfile


from mock import patch, MagicMock
from unittest import TestCase
import pandas as pd
try:
    from StringIO import StringIO
except ImportError:  # pragma nocover
    from io import StringIO

from pandashells.bin.p_df import (
    needs_plots,
    get_modules_and_shortcuts,
    framify,
    process_command,
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
        self.assertTrue(isinstance(out, pd.DataFrame))

    def test_series_to_dataframe(self):
        cmd = ''
        df = pd.Series({'a': 1})
        out = framify(cmd, df)
        self.assertTrue(isinstance(out, pd.DataFrame))

    def test_list_to_dataframe(self):
        cmd = ''
        df = [1, 2, 3]
        out = framify(cmd, df)
        self.assertTrue(isinstance(out, pd.DataFrame))

    @patch('pandashells.bin.p_df.sys')
    def test_number_to_dataframe(self, sys_mock):
        cmd = ''
        df = 7
        sys_mock.stderr = MagicMock(write=MagicMock())
        sys_mock.exit = MagicMock()
        framify(cmd, df)
        self.assertTrue(sys_mock.stderr.write.called)
        self.assertTrue(sys_mock.exit.called)


class ProcessCommandTests(TestCase):
    def setUp(self):
        self.df = pd.DataFrame([
            {'a': 1, 'b': 10},
            {'a': 2, 'b': 20},
            {'a': 3, 'b': 30},
            {'a': 4, 'b': 40},
        ])

    def test_col_assignement(self):
        args = MagicMock()
        cmd = 'df["c"] = 2 * df["a"]'
        df = process_command(args, cmd, self.df)
        self.assertEqual(df.c.iloc[0], 2)

    @patch('pandashells.bin.p_df.sys')
    @patch('pandashells.bin.p_df.exec_plot_command')
    def test_plot_needed(self, exec_plot_mock, sys_mock):
        args = MagicMock()
        sys_mock.exit = MagicMock()
        cmd = 'df.plot(x="a", y="b")'
        process_command(args, cmd, self.df)
        self.assertTrue(exec_plot_mock.called)
        self.assertTrue(sys_mock.exit.called)

    def test_regular_command(self):
        args = MagicMock()
        cmd = 'df.a.value_counts()'
        df = process_command(args, cmd, self.df)

        # this line is needed so tests pass for different pandas version
        df = df.rename(columns={0: 'a'})

        self.assertEqual(set(df.index), {1, 2, 3, 4})
        self.assertEqual(set(df['a']), {1})


class IntegrationTests(TestCase):
    def setUp(self):
        self.df = pd.DataFrame([
            {'a': 1, 'b': 10},
            {'a': 2, 'b': 20},
            {'a': 3, 'b': 30},
            {'a': 4, 'b': 40},
        ])

    def get_command_result(self, cmd, as_table=False):
        p = subprocess.Popen(
            ['bash', '-c', cmd],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if as_table:
            stdout, stderr = p.communicate(
                self.df.to_string(index=False).encode('utf-8'))
        else:
            stdout, stderr = p.communicate(
                self.df.to_csv(index=False).encode('utf-8'))
        return stdout.decode('utf-8').strip()

    def test_no_command(self):
        cmd = 'p.df'
        df = pd.read_csv(StringIO(self.get_command_result(cmd)))
        self.assertEqual(list(df.a), [1, 2, 3, 4])

    def test_names(self):
        cmd = 'p.df --names  x y'
        df = pd.read_csv(StringIO(self.get_command_result(cmd)))
        self.assertEqual(list(df.columns), ['x', 'y'])

    def test_multiple_commands(self):
        cmd = """p.df  'df["y"] = -df.y'  'df["z"] = df["y"]' --names  x y"""
        df = pd.read_csv(StringIO(self.get_command_result(cmd)))
        self.assertTrue(all(df.z < 0))

    def test_input_table(self):
        cmd = 'p.df -i table'
        df = pd.read_csv(StringIO(
            self.get_command_result(cmd, as_table=True)))
        self.assertEqual(list(df.columns), ['a', 'b'])

    def test_output_table(self):
        cmd = 'p.df -o table'
        df = pd.read_csv(
            StringIO(self.get_command_result(cmd)), delimiter=r'\s+')
        self.assertEqual(list(df.columns), ['a', 'b'])

    def test_plotting(self):
        dir_name = tempfile.mkdtemp()
        file_name = os.path.join(dir_name, 'deleteme.png')
        cmd = """p.df 'df.plot(x="a", y="b")' --savefig {}""".format(file_name)
        self.get_command_result(cmd)
        file_existed = os.path.isfile(file_name)
        os.system('rm -rf {}'.format(dir_name))
        self.assertTrue(file_existed)
