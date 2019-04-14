#! /usr/bin/env python
import os
import tempfile
import shutil
import warnings
warnings.filterwarnings("ignore")
from unittest import TestCase
from pandashells.lib import plot_lib, arg_lib
import argparse
from mock import patch, MagicMock
import matplotlib as mpl
import pylab as pl
import pandas as pd
from dateutil.parser import parse
warnings.resetwarnings()


class PlotLibTests(TestCase):
    def setUp(self):
        pl.plot(range(10))
        self.dir_name = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir_name)
        pl.clf()

    @patch('pandashells.lib.plot_lib.pl.show')
    def test_show_calls_pylab_show(self, show_mock):
        """show() call pylab.show()
        """
        args = MagicMock(savefig=[])
        plot_lib.show(args)
        self.assertTrue(show_mock.called)

    def test_show_creates_png_file(self):
        """show() saves a png file
        """
        file_name = os.path.join(self.dir_name, 'plot.png')
        args = MagicMock(savefig=[file_name])

        plot_lib.show(args)

        self.assertTrue(os.path.isfile(file_name))

    def test_show_creates_html_file(self):
        """show() saves a png file
        """
        file_name = os.path.join(self.dir_name, 'plot.html')
        args = MagicMock(savefig=[file_name])

        xlabel = 'my_xlabel_string'
        pl.xlabel(xlabel)
        plot_lib.show(args)
        with open(file_name) as f:
            self.assertTrue(xlabel in f.read())

    def test_set_plot_styling(self):
        """set_plot_styling() alters mpl.rcParams
        """
        args = MagicMock(
            plot_context=['talk'],
            plot_theme=['darkgrid'],
            plot_palette=['muted'],
        )
        mpl.rcParams['axes.labelsize'] = 1
        mpl.rcParams['axes.titlesize'] = 1
        rc_pre = dict(mpl.rcParams)
        plot_lib.set_plot_styling(args)
        rc_post = dict(mpl.rcParams)
        self.assertNotEqual(
            rc_pre['axes.labelsize'], rc_post['axes.labelsize'])

        self.assertNotEqual(
            rc_pre['axes.titlesize'], rc_post['axes.titlesize'])

    def test_set_plot_limits_no_args(self):
        """set_limits() properly does nothing when nothing specified
        """
        args = MagicMock(savefig='', xlim=[], ylim=[])
        plot_lib.set_limits(args)
        self.assertEqual(pl.gca().get_xlim(), (-0.45, 9.45))
        self.assertEqual(pl.gca().get_ylim(), (-0.45, 9.45))

    def test_set_plot_limits(self):
        """set_limits() properly sets limits
        """
        args = MagicMock(savefig='', xlim=[-2, 2], ylim=[-3, 3])
        plot_lib.set_limits(args)
        self.assertEqual(pl.gca().get_xlim(), (-2.0, 2.0))
        self.assertEqual(pl.gca().get_ylim(), (-3.0, 3.0))

    def test_set_log_scale(self):
        args = MagicMock(savefig='', xlog=True, ylog=True)
        plot_lib.set_scale(args)
        self.assertEqual(pl.gca().get_xscale(), 'log')
        self.assertEqual(pl.gca().get_yscale(), 'log')

    def test_keep_lin_scale(self):
        args = MagicMock(savefig='', xlog=False, ylog=False)
        plot_lib.set_scale(args)
        self.assertEqual(pl.gca().get_xscale(), 'linear')
        self.assertEqual(pl.gca().get_yscale(), 'linear')

    def test_set_labels_titles_no_args(self):
        """set_labels_title() properly does nothing when nothing specified
        """
        args = MagicMock(savefig='', title=[], xlabel=[], ylabel=[])
        plot_lib.set_labels_title(args)
        self.assertEqual(pl.gca().get_title(), '')
        self.assertEqual(pl.gca().get_xlabel(), '')
        self.assertEqual(pl.gca().get_ylabel(), '')

    def test_set_labels_titles(self):
        """set_labels_title() properly sets labels and titles
        """
        args = MagicMock(savefig='', title=['t'], xlabel=['x'], ylabel=['y'])
        plot_lib.set_labels_title(args)
        self.assertEqual(pl.gca().get_title(), 't')
        self.assertEqual(pl.gca().get_xlabel(), 'x')
        self.assertEqual(pl.gca().get_ylabel(), 'y')

    @patch('pandashells.lib.plot_lib.pl.legend')
    def test_set_legend_no_args(self, legend_mock):
        """set_legend() properly does nothing when nothing specified
        """
        args = MagicMock(savefig='', legend=[])
        plot_lib.set_legend(args)
        self.assertFalse(legend_mock.called)

    @patch('pandashells.lib.plot_lib.pl.legend')
    def test_set_legend_best(self, legend_mock):
        """set_legend() properly calls legend when specified
        """
        args = MagicMock(savefig='', legend=['best'])
        plot_lib.set_legend(args)
        legend_mock.assert_called_with(loc='best')

    @patch('pandashells.lib.plot_lib.pl.legend')
    def test_set_legend_int(self, legend_mock):
        """set_legend() properly calls legend when specified
        """
        args = MagicMock(savefig='', legend=['3'])
        plot_lib.set_legend(args)
        legend_mock.assert_called_with(loc=3)

    def test_set_grid_no_grid(self):
        """set_grid() properly does nothing when no_grid set
        """
        args = MagicMock(savefig='', no_grid=True)
        plot_lib.set_grid(args)
        self.assertFalse(pl.gca().xaxis._gridOnMajor)

    def test_set_grid_with_grid(self):
        """set_grid() properly sets grid when specified
        """
        args = MagicMock(savefig='', no_grid=False)
        plot_lib.set_grid(args)
        self.assertTrue(pl.gca().xaxis._gridOnMajor)

    @patch('pandashells.lib.plot_lib.sys.stderr')
    @patch('pandashells.lib.plot_lib.sys.exit')
    def test_ensure_xy_args_bad(self, exit_mock, stderr_mock):
        """ensure_xy_args() exits when args are bad
        """
        stderr_mock.write = MagicMock()
        args = MagicMock(x=None, y=True)
        plot_lib.ensure_xy_args(args)
        self.assertTrue(exit_mock.called)

    @patch('pandashells.lib.plot_lib.sys.stderr')
    @patch('pandashells.lib.plot_lib.sys.exit')
    def test_ensure_xy_args_good(self, exit_mock, stderr_mock):
        """ensure_xy_args() doesn't exit when args okay
        """
        stderr_mock.write = MagicMock()
        args = MagicMock(x=None, y=None)
        plot_lib.ensure_xy_args(args)
        self.assertFalse(exit_mock.called)

    @patch('pandashells.lib.plot_lib.sys.stderr')
    @patch('pandashells.lib.plot_lib.sys.exit')
    def test_ensure_xy_omission_state_bad(self, exit_mock, stderr_mock):
        """ensure_xy_omission_state() identifies bad inputs
        """
        stderr_mock.write = MagicMock()
        args = MagicMock(x=None, y=None)
        df = MagicMock(columns=[1, 2, 3])
        plot_lib.ensure_xy_omission_state(args, df)
        self.assertTrue(exit_mock.called)

    @patch('pandashells.lib.plot_lib.sys.stderr')
    @patch('pandashells.lib.plot_lib.sys.exit')
    def test_ensure_xy_omission_state_good(self, exit_mock, stderr_mock):
        """ensure_xy_omission_state() identifies bad inputs
        """
        stderr_mock.write = MagicMock()
        args = MagicMock(x=None, y=None)
        df = MagicMock(columns=[1, 2])
        plot_lib.ensure_xy_omission_state(args, df)
        self.assertFalse(exit_mock.called)

    def test_autofill_plot_fields_and_labels_do_nothing(self):
        """autofill_plot_fields_and_labels does no filling
        """
        args = MagicMock(x=None, xlabel='xpre', ylabel='ypre')
        df = MagicMock(columns=[1])

        plot_lib.autofill_plot_fields_and_labels(args, df)
        self.assertEqual(args.xlabel, 'xpre')
        self.assertEqual(args.ylabel, 'ypre')

    def test_autofill_plot_fields_and_labels_2_cols(self):
        """autofill_plot_labels() appropriately handles 2 column frame
        """
        args = MagicMock(x=None, xlabel=None, ylabel=None)
        df = MagicMock(columns=['x', 'y'])

        plot_lib.autofill_plot_fields_and_labels(args, df)
        self.assertEqual(args.x, ['x'])
        self.assertEqual(args.y, ['y'])
        self.assertEqual(args.xlabel, ['x'])
        self.assertEqual(args.ylabel, ['y'])

    def test_str_to_date_float(self):
        x = pd.Series([1., 2., 3.])
        self.assertEqual(list(x), list(plot_lib.str_to_date(x)))

    def test_str_to_date_str(self):
        x = pd.Series(['1/1/2014', '1/2/2014', '1/3/2014'])
        expected = [parse(e) for e in x]
        self.assertEqual(expected, list(plot_lib.str_to_date(x)))

    @patch('pandashells.lib.plot_lib.pl.plot')
    def test_draw_traces(self, plot_mock):
        args = MagicMock(savefig='', x='x', y='y')
        df = pd.DataFrame([[1, 1], [2, 2]], columns=['x', 'y'])
        plot_lib.draw_traces(args, df)
        self.assertTrue(plot_mock.called)

    def test_draw_xy_plot(self):
        """draw_xy_plot() properly produces an output html file
        """
        out_file = os.path.join(self.dir_name, 'test.html')
        argv = (
            'p.plot -x x -y btrace ctrace -s o- --xlabel myxlabel '
            '--ylabel myylabel --title mytitle --theme darkgrid '
            '--context talk --palette muted -a .5 --nogrid '
            '--legend best --xlim 0 10 --ylim -10 10 '
            '--savefig {}'.format(out_file)
        ).split()
        with patch('pandashells.lib.plot_lib.sys.argv', argv):
            pl.clf()
            df = pd.DataFrame(
                {
                    'x': range(10),
                    'btrace': [-x for x in range(10)],
                    'ctrace': [x for x in range(10)]
                })
            parser = argparse.ArgumentParser()
            arg_lib.add_args(
                parser, 'io_in', 'xy_plotting', 'decorating')

            parser.add_argument(
                "-a", "--alpha", help="Set opacity", nargs=1, default=[1.],
                type=float)
            args = parser.parse_args()
            plot_lib.draw_xy_plot(args, df)
            with open(out_file) as f:
                html = f.read()
                self.assertTrue('myxlabel' in html)
                self.assertTrue('myylabel' in html)
                self.assertTrue('mytitle' in html)
                self.assertTrue('btrace' in html)
                self.assertTrue('ctrace' in html)
                self.assertTrue('1' in html)
                self.assertTrue('10' in html)
