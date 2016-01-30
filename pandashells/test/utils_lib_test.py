#! /usr/bin/env python

from unittest import TestCase

import datetime
import time
from pandashells.lib.utils_lib import Timer, TimerResult
from mock import patch


class TimerResultTests(TestCase):
    def test_repr(self):
        starting = datetime.datetime(2000, 1, 1)
        ending = datetime.datetime(2000, 1, 2)
        res = TimerResult('label', starting, ending, 1)
        self.assertEqual(res.__repr__(), '__time__,1,label')


class TimerTests(TestCase):
    @patch('pandashells.lib.utils_lib.OutStream.write')
    def test_timer(self, write_mock):
        with Timer('test_timer'):
            time.sleep(.1)
        self.assertTrue('test_timer' in write_mock.call_args_list[1][0][0])
