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

