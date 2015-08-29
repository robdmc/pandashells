#! /usr/bin/env python
from unittest import TestCase
from pandashells.lib.module_checker_lib import check_for_modules
from pandashells.lib import module_checker_lib
from mock import patch


class ModuleCheckerTests(TestCase):
    def setUp(self):
        module_checker_lib.CMD_DICT['fakemodule1'] = 'pip install fakemodule1'
        module_checker_lib.CMD_DICT['fakemodule2'] = 'pip install fakemodule2'
        module_checker_lib.CMD_DICT['os'] = 'part of standard module'

    def test_check_for_modules_unrecognized(self):
        """
        check_for_modules() raises error when module is unrecognized
        """
        with self.assertRaises(ValueError):
            check_for_modules(['not_a_module'])

    @patch('pandashells.lib.module_checker_lib.importlib.import_module')
    def test_check_for_modules_no_modules(self, import_module_mock):
        """
        check_for_modules() does nothing when module list is empty
        """
        check_for_modules([])
        self.assertFalse(import_module_mock.called)

    def test_check_for_modules_existing_module(self):
        """
        check_for_modules() successfully finds existing module
        """
        check_for_modules(['os'])

    def test_check_for_modules_bad(self):
        """
        check_for_modules() correctly identifies missing modules
        """
        with self.assertRaises(SystemExit):
            check_for_modules(['fakemodule1', 'fakemodule2'])
