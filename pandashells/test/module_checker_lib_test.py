#! /usr/bin/env python
import os
import json
from unittest import TestCase
from pandashells.lib.module_checker_lib import check_for_modules
import argparse
from mock import patch, MagicMock, call


@patch('pandashells.lib.module_checker_lib.importlib.import_module')
class ModuleCheckerTests(TestCase):
    def test_check_for_modules_no_modules(self, import_module_mock):
        check_for_modules()
        self.assertFalse(import_module_mock.called)


