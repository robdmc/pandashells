#! /usr/bin/env python
import os
import sys
import json
import tempfile
import shutil
from unittest import TestCase
from pandashells.lib import parallel_lib
import argparse
from mock import patch, MagicMock, call
import matplotlib as mpl
import pylab as pl
import pandas as pd
import datetime
import multiprocessing as mp


class ParallelLibTests(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('pandashells.lib.parallel_lib.sys.stdout')
    @patch('pandashells.lib.parallel_lib.csv.DictWriter')
    def test_precommand_verbose_print_not_verbose_no_supress(
            self, DictWriter_mock, stdout_mock):
        DictWriter_mock.return_value = MagicMock()
        stdout_mock.flush = MagicMock()
        stdout_mock.write = MagicMock()
        writer_mock = DictWriter_mock.return_value
        writer_mock.writerow = MagicMock()

        verbose, suppress_cmd = False, False
        job_num, job_tot = 1, 1
        cmd = 'echo hello'
        parallel_lib.pre_command_verbose_print(
            verbose, suppress_cmd, cmd, job_num, job_tot)
        stdout_mock.write.assert_called_with('echo hello\n')

    @patch('pandashells.lib.parallel_lib.sys.stdout')
    @patch('pandashells.lib.parallel_lib.csv.DictWriter')
    def test_precommand_verbose_print_verbose_supress(
            self, DictWriter_mock, stdout_mock):
        DictWriter_mock.return_value = MagicMock()
        stdout_mock.flush = MagicMock()
        stdout_mock.write = MagicMock()
        writer_mock = DictWriter_mock.return_value
        writer_mock.writerow = MagicMock()

        verbose, suppress_cmd = True, True
        job_num, job_tot = 1, 1
        cmd = 'echo hello'
        parallel_lib.pre_command_verbose_print(
            verbose, suppress_cmd, cmd, job_num, job_tot)
        kwarg = writer_mock.writerow.call_args_list[0][0][0]
        self.assertTrue(writer_mock.writerow.called)
        self.assertEqual(kwarg['cmd'], '')

    @patch('pandashells.lib.parallel_lib.sys.stdout')
    @patch('pandashells.lib.parallel_lib.csv.DictWriter')
    def test_precommand_verbose_print_verbose_no_supress(
            self, DictWriter_mock, stdout_mock):
        DictWriter_mock.return_value = MagicMock()
        stdout_mock.flush = MagicMock()
        stdout_mock.write = MagicMock()
        writer_mock = DictWriter_mock.return_value
        writer_mock.writerow = MagicMock()

        verbose, suppress_cmd = True, False
        job_num, job_tot = 1, 1
        cmd = 'echo hello'
        parallel_lib.pre_command_verbose_print(
            verbose, suppress_cmd, cmd, job_num, job_tot)
        kwarg = writer_mock.writerow.call_args_list[0][0][0]
        self.assertTrue(writer_mock.writerow.called)
        self.assertEqual(kwarg['cmd'], 'echo hello')

    @patch('pandashells.lib.parallel_lib.sys.stdout')
    @patch('pandashells.lib.parallel_lib.csv.DictWriter')
    def test_precommand_verbose_print_not_verbose_supress(
            self, DictWriter_mock, stdout_mock):
        DictWriter_mock.return_value = MagicMock()
        stdout_mock.flush = MagicMock()
        stdout_mock.write = MagicMock()
        writer_mock = DictWriter_mock.return_value
        writer_mock.writerow = MagicMock()

        verbose, suppress_cmd = False, False
        job_num, job_tot = 1, 1
        cmd = 'echo hello'
        parallel_lib.pre_command_verbose_print(
            verbose, suppress_cmd, cmd, job_num, job_tot)
        stdout_mock.write.assert_called_with('echo hello\n')

    @patch('pandashells.lib.parallel_lib.csv.DictWriter')
    def test_post_command_verbose_print_non_verbose(
            self, DictWriter_mock):
        DictWriter_mock.return_value = MagicMock()
        writer_mock = DictWriter_mock.return_value
        writer_mock.writerow = MagicMock()

        then = datetime.datetime(2014, 1, 1, 12, 0, 0)
        now = datetime.datetime(2014, 1, 1, 12, 0, 1)
        verbose = False
        cmd = 'echo hello'
        rec = {}
        parallel_lib.post_command_verbose_print(now, then, rec, verbose)
        self.assertFalse(writer_mock.writerow.called)

    @patch('pandashells.lib.parallel_lib.csv.DictWriter')
    def test_post_command_verbose_print_verbose(
            self, DictWriter_mock):
        DictWriter_mock.return_value = MagicMock()
        writer_mock = DictWriter_mock.return_value
        writer_mock.writerow = MagicMock()

        then = datetime.datetime(2014, 1, 1, 12, 0, 0)
        now = datetime.datetime(2014, 1, 1, 12, 0, 7)
        verbose = True
        cmd = 'echo hello'
        rec = {}
        parallel_lib.post_command_verbose_print(now, then, rec, verbose)
        kwarg = writer_mock.writerow.call_args_list[0][0][0]
        self.assertAlmostEqual(kwarg['duration_sec'], 7)

    @patch('pandashells.lib.parallel_lib.sys.stdout')
    def test_verbose_writer(self, stdout_mock):
        stdout_mock.write = MagicMock()
        verbose, suppress_cmd = True, False
        cmd = 'echo hello'
        job_num, job_tot = 1, 1
        with parallel_lib.verbose_writer(verbose, suppress_cmd, cmd, job_num,
                                         job_tot):
            pass
        self.assertEqual(len(stdout_mock.write.call_args_list), 2)

    @patch('pandashells.lib.parallel_lib.sys.stdout')
    def test_worker(self, stdout_mock):
        stdout_mock.write = MagicMock()

        verbose, suppress_cmd = True, True
        suppress_stdout, suppress_stderr = True, True
        cmd_list = ['echo 1', 'echo 2', 'echo 3']
        job_tot, keep_alive = len(cmd_list), True

        queue = mp.JoinableQueue()
        for job_num, cmd in enumerate(cmd_list):
            queue.put((job_num, job_tot, cmd, keep_alive))
        queue.put((0, 0, '', False))
        parallel_lib.worker(
            queue, verbose, suppress_cmd, suppress_stdout, suppress_stderr)
        self.assertEqual(len(stdout_mock.write.call_args_list), 6)






