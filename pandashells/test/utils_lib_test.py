#! /usr/bin/env python

from unittest import TestCase

import time
from pandashells.lib.utils_lib import Timer
from mock import patch


class TimerTests(TestCase):
    @patch('pandashells.lib.utils_lib.OutStream.write')
    def test_timer(self, write_mock):
        with Timer('test_timer'):
            time.sleep(.1)
        self.assertTrue('test_timer' in write_mock.call_args_list[0][0][0])
