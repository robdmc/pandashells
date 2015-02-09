#! /usr/bin/env python
import sys
from unittest import TestCase
from pandashells.lib import parallel_lib
from mock import patch, MagicMock
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
        sys.stdout = sys.__stdout__

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
        sys.stdout = sys.__stdout__

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
        sys.stdout = sys.__stdout__

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
        sys.stdout = sys.__stdout__

    @patch('pandashells.lib.parallel_lib.csv.DictWriter')
    def test_post_command_verbose_print_non_verbose(
            self, DictWriter_mock):
        DictWriter_mock.return_value = MagicMock()
        writer_mock = DictWriter_mock.return_value
        writer_mock.writerow = MagicMock()

        then = datetime.datetime(2014, 1, 1, 12, 0, 0)
        now = datetime.datetime(2014, 1, 1, 12, 0, 1)
        verbose = False
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
        sys.stdout = sys.__stdout__

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
        sys.stdout = sys.__stdout__

    @patch('pandashells.lib.parallel_lib.mp.cpu_count', return_value=2)
    def test_number_of_jobs_explicit(self, stdout_mock):
        self.assertEqual(parallel_lib.get_number_of_jobs(
            njobs=6, assume_hyperthread=True), 6)

    @patch('pandashells.lib.parallel_lib.mp.cpu_count', return_value=2)
    def test_number_of_jobs_hyperthread_2(self, stdout_mock):
        self.assertEqual(parallel_lib.get_number_of_jobs(
            njobs=None, assume_hyperthread=True), 1)

    @patch('pandashells.lib.parallel_lib.mp.cpu_count', return_value=3)
    def test_number_of_jobs_hyperthread_3(self, stdout_mock):
        self.assertEqual(parallel_lib.get_number_of_jobs(
            njobs=None, assume_hyperthread=True), 3)

    @patch('pandashells.lib.parallel_lib.csv.DictWriter')
    def test_master_verbose_writer_verbose_no_suppress(self, DictWriter_mock):
        parallel_lib.master_verbose_writer(True, False)
        DictWriter_mock.assert_called_with(
            sys.stdout,
            [
                '__job__activity',
                'job_num',
                'job_tot',
                'duration_sec',
                'duration_min',
                'pid',
                'time_stamp',
            ]
        )

    @patch('pandashells.lib.parallel_lib.csv.DictWriter')
    def test_master_verbose_writer_verbose_suppress(self, DictWriter_mock):
        parallel_lib.master_verbose_writer(True, True)
        DictWriter_mock.assert_called_with(
            sys.stdout,
            [
                '__job__activity',
                'job_num',
                'job_tot',
                'duration_sec',
                'duration_min',
                'pid',
            ]
        )

    @patch('pandashells.lib.parallel_lib.csv.DictWriter')
    def test_master_verbose_writer_no_verbose(self, DictWriter_mock):
        parallel_lib.master_verbose_writer(False, True)
        self.assertFalse(DictWriter_mock.called)

    def test_parallel(self):
        cmd = "python -c 'import time; time.sleep(.75)'"
        cmd_list = [cmd for nn in range(4)]
        then = datetime.datetime.now()
        parallel_lib.parallel(
            cmd_list, njobs=1, suppress_stdout=True, suppress_stderr=True,
            assume_hyperthread=True,
            suppress_cmd=True,
        )
        seconds_single = (datetime.datetime.now() - then).total_seconds()

        then = datetime.datetime.now()
        parallel_lib.parallel(
            cmd_list, njobs=4, suppress_stdout=True, suppress_stderr=True,
            assume_hyperthread=True,
            suppress_cmd=True,
        )
        seconds_multi = (datetime.datetime.now() - then).total_seconds()
        self.assertTrue(seconds_single / seconds_multi >= 3.)
