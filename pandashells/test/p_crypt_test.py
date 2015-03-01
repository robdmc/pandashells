#! /usr/bin/env python
import copy
from contextlib import contextmanager
import json
import os
import sys
import tempfile
import shutil


from mock import patch, MagicMock
from unittest import TestCase

from pandashells.lib import config_lib
from pandashells.bin.p_crypt import main

#TODO: Mock out the add_args methods in failing tests to get them to pass

class MainTests(TestCase):

    @patch(
        'pandashells.bin.p_crypt.sys.argv',
        'p.crypt -i my_in -o my_out'.split())
    @patch('pandashells.bin.p_crypt.os.system')
    @patch('pandashells.bin.p_crypt.os.path.isfile')
    def test_proper_encrypt(self, isfile_mock, system_mock):
        isfile_mock.return_value = True
        main()
        system_mock.assert_called_with(
            'cat my_in | openssl enc -aes-256-cbc -salt  > my_out')

    @patch(
        'pandashells.bin.p_crypt.sys.argv',
        'p.crypt -i my_in -o my_out -v'.split())
    @patch('pandashells.bin.p_crypt.sys.stdout')
    @patch('pandashells.bin.p_crypt.os.system')
    @patch('pandashells.bin.p_crypt.os.path.isfile')
    def test_proper_encrypt_verbose(
            self, isfile_mock, system_mock, stdout_mock):
        stdout_mock.write = MagicMock()
        isfile_mock.return_value = True
        main()
        system_mock.assert_called_with(
            'cat my_in | openssl enc -aes-256-cbc -salt  > my_out')
        self.assertTrue(stdout_mock.write.called)



    @patch(
        'pandashells.bin.p_crypt.sys.argv',
        'p.crypt -i my_in -o my_out --password xx'.split())
    @patch('pandashells.bin.p_crypt.os.system')
    @patch('pandashells.bin.p_crypt.os.path.isfile')
    def test_proper_encypt_with_password(self, isfile_mock, system_mock):
        isfile_mock.return_value = True
        main()
        system_mock.assert_called_with(
            "cat my_in | openssl enc -aes-256-cbc -salt -k 'xx' > my_out")

    @patch(
        'pandashells.bin.p_crypt.sys.argv',
        'p.crypt -i my_in -o my_out --password xx'.split())
    @patch('pandashells.bin.p_crypt.sys.stderr')
    @patch('pandashells.bin.p_crypt.os.system')
    @patch('pandashells.bin.p_crypt.os.path.isfile')
    def test_proper_encypt_no_input_file(
            self, isfile_mock, stderr_mock, system_mock):
        isfile_mock.return_value = False
        with self.assertRaises(SystemExit):
            main()

    @patch(
        'pandashells.bin.p_crypt.sys.argv',
        'p.crypt -i my_in -o my_out -d'.split())
    @patch('pandashells.bin.p_crypt.os.system')
    @patch('pandashells.bin.p_crypt.os.path.isfile')
    def test_proper_decrypt(self, isfile_mock, system_mock):
        isfile_mock.return_value = True
        main()
        system_mock.assert_called_with(
            'cat my_in | openssl enc -d -aes-256-cbc  > my_out')















    #@patch(
    #    'pandashells.bin.p_config.sys.argv',
    #    [
    #        'p.crypt',
    #        '--force_defaults',
    #    ]
    #)
    #def test_force_defaults(self):
    #    with mute_output():
    #        main()
    #    with open(config_lib.CONFIG_FILE_NAME) as config_file:
    #        config_dict = json.loads(config_file.read())
    #        self.assertEqual(config_dict, config_lib.DEFAULT_DICT)

    #@patch(
    #    'pandashells.bin.p_config.sys.argv',
    #    [
    #        'p.config',
    #        '--io_output_na_rep', '',
    #        '--io_input_type', 'table',
    #    ]
    #)
    #def test_custom(self):
    #    with mute_output():
    #        main()
    #    with open(config_lib.CONFIG_FILE_NAME) as config_file:
    #        expected_dict = copy.copy(config_lib.DEFAULT_DICT)
    #        expected_dict['io_output_na_rep'] = ''
    #        expected_dict['io_input_type'] = 'table'

    #        config_dict = json.loads(config_file.read())
    #        self.assertEqual(config_dict, expected_dict)
