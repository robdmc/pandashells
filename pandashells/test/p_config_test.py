#! /usr/bin/env python
import copy
from contextlib import contextmanager
import json
import os
import sys


from mock import patch, MagicMock
from unittest import TestCase

from pandashells.lib import config_lib
from pandashells.bin.p_config import (
    main,
)


@contextmanager
def mute_output():
    sys.stdout = MagicMock()
    yield
    sys.stdout = sys.__stdout__


class MainTests(TestCase):
    # tests wipe out config file (might want to change this later)
    def setUp(self):
        if os.path.isfile(config_lib.CONFIG_FILE_NAME):
            cmd = 'rm {} 2>/dev/null'.format(config_lib.CONFIG_FILE_NAME)
            os.system(cmd)

    def tearDown(self):
        if os.path.isfile(config_lib.CONFIG_FILE_NAME):
            cmd = 'rm {} 2>/dev/null'.format(config_lib.CONFIG_FILE_NAME)
            os.system(cmd)

    @patch(
        'pandashells.bin.p_config.sys.argv',
        [
            'p.config',
            '--force_defaults',
        ]
    )
    def test_force_defaults(self):
        with mute_output():
            main()
        with open(config_lib.CONFIG_FILE_NAME) as config_file:
            config_dict = json.loads(config_file.read())
            self.assertEqual(config_dict, config_lib.DEFAULT_DICT)

    @patch(
        'pandashells.bin.p_config.sys.argv',
        [
            'p.config',
            '--io_output_na_rep', '',
            '--io_input_type', 'table',
        ]
    )
    def test_custom(self):
        with mute_output():
            main()
        with open(config_lib.CONFIG_FILE_NAME) as config_file:
            expected_dict = copy.copy(config_lib.DEFAULT_DICT)
            expected_dict['io_output_na_rep'] = ''
            expected_dict['io_input_type'] = 'table'

            config_dict = json.loads(config_file.read())
            self.assertEqual(config_dict, expected_dict)
