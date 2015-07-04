#! /usr/bin/env python
from unittest import TestCase
import sys

from mock import patch, MagicMock

from pandashells.bin.p_parallel import main


class TestMain(TestCase):
    @patch(
        'pandashells.bin.p_parallel.sys.argv', 'p.parallel -n 1'.split())
    @patch(
        'pandashells.bin.p_parallel.parallel_lib')
    def test_parallel_called(self, parallel_mock):
        sys.stdin = MagicMock()
        main()
        sys.stdin = sys.__stdin__
        self.assertTrue(parallel_mock.parallel.called)
