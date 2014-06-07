#! /usr/bin/env python

import os
import sys
import unittest

fileDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fileDir, '../..'))

from  ptools.lib import module_checker_lib as mod

class module_checker_tests(unittest.TestCase):

    def setUp(self):
        mod.CMD_DICT.update({'fakemodule': 'pip install fakemodule'})

    def tearDown(self):
        pass

    def test_check_for_existing_module(self):
        importsOkay = mod.check_for_modules(['os'])
        self.assertEqual(importsOkay, True)

    def test_check_for_missing_module(self):
        importsOkay = mod.check_for_modules(['fakemodule'])
        self.assertEqual(importsOkay, False)
