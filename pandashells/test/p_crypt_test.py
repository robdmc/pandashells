#! /usr/bin/env python

from mock import patch, MagicMock
from unittest import TestCase

from pandashells.bin.p_crypt import main


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
            'cat my_in | openssl enc -aes-256-cbc -pbkdf2 -salt  > my_out')

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
            'cat my_in | openssl enc -aes-256-cbc -pbkdf2 -salt  > my_out')
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
            "cat my_in | openssl enc -aes-256-cbc -pbkdf2 -salt -k 'xx' > my_out")

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
            'cat my_in | openssl enc -d -aes-256-cbc  -pbkdf2 > my_out')
