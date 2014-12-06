#! /usr/bin/env python
import os
import json
import tempfile
import shutil
from unittest import TestCase
from pandashells.lib import plot_lib
import argparse
from mock import patch, MagicMock, call
import matplotlib as mpl
import pylab as pl


class PlotLibTests(TestCase):
    def setUp(self):
        self.dir_name = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir_name)


    @patch('pandashells.lib.plot_lib.pl.show')
    def test_show_calls_pylab_show(self, show_mock):
        """show() call pylab.show()
        """
        args = MagicMock(savefig=[])
        pl.plot(range(10))
        plot_lib.show(args)
        self.assertTrue(show_mock.called)

    def test_show_creates_png_file(self):
        """show() saves a png file
        """
        file_name = os.path.join(self.dir_name, 'plot.png')
        args = MagicMock(savefig=[file_name])

        pl.plot(range(10))
        plot_lib.show(args)

        self.assertTrue(os.path.isfile(file_name))

    def test_show_creates_html_file(self):
        """show() saves a png file
        """
        file_name = os.path.join(self.dir_name, 'plot.html')
        args = MagicMock(savefig=[file_name])

        pl.plot(range(10))
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
        rc_pre = dict(mpl.rcParams)
        plot_lib.set_plot_styling(args)
        rc_post = dict(mpl.rcParams)
        self.assertNotEqual(
            rc_pre['axes.color_cycle'], rc_post['axes.color_cycle'])
        self.assertNotEqual(
            rc_pre['axes.labelsize'], rc_post['axes.labelsize'])

        self.assertNotEqual(
            rc_pre['axes.titlesize'], rc_post['axes.titlesize'])

    def test_set_plot_limits_no_args(self):
        """set_limits() properly does nothing when nothing specified
        """
        args = MagicMock(savefig='', xlim=[], ylim=[])
        pl.plot(range(10))
        plot_lib.set_limits(args)
        self.assertEqual(pl.gca().get_xlim(), (0.0, 9.0))
        self.assertEqual(pl.gca().get_ylim(), (0.0, 9.0))

    def test_set_plot_limits(self):
        """set_limits() properly sets limits
        """
        args = MagicMock(savefig='', xlim=[-2, 2], ylim=[-3, 3])
        pl.plot(range(10))
        plot_lib.set_limits(args)
        self.assertEqual(pl.gca().get_xlim(), (-2.0, 2.0))
        self.assertEqual(pl.gca().get_ylim(), (-3.0, 3.0))

    def test_set_labels_titles_no_args(self):
        """set_labels_title() properly does nothing when nothing specified
        """
        args = MagicMock(savefig='', title=[], xlabel=[], ylabel=[])
        pl.plot(range(10))
        plot_lib.set_labels_title(args)
        self.assertEqual(pl.gca().get_title(), '')
        self.assertEqual(pl.gca().get_label(), '')
        self.assertEqual(pl.gca().get_title(), '')

    def test_set_labels_titles(self):
        """set_labels_title() properly sets labels and titles
        """
        args = MagicMock(savefig='', title=['t'], xlabel=['x'], ylabel=['y'])
        pl.plot(range(10))
        plot_lib.set_labels_title(args)
        self.assertEqual(pl.gca().get_title(), 't')
        self.assertEqual(pl.gca().get_xlabel(), 'x')
        self.assertEqual(pl.gca().get_ylabel(), 'y')

    def test_set_grid_no_grid(self):
        """set_grid() properly does nothing when no_grid set
        """
        args = MagicMock(savefig='', no_grid=True)
        pl.plot(range(10))
        plot_lib.set_grid(args)
        self.assertFalse(pl.gca().xaxis._gridOnMajor)

    def test_set_grid_with_grid(self):
        """set_grid() properly sets grid when specified
        """
        args = MagicMock(savefig='', no_grid=False)
        pl.plot(range(10))
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

        """
        need to test autofill_plot_labels next
        """

