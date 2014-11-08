#! /usr/bin/env python
import os
import unittest
from pandashells.lib import config_lib

class GlobalArgTests(unittest.TestCase):
    def test_home_path_looks_right(self):
        """
        The path to the users home directory looks right
        """
        home = os.path.expanduser('~')
        self.assertEqual(config_lib.HOME, home)

    def test_default_opt_dict_exists(self):
        """
        The dictionary of default options exists
        """
        self.assertTrue(len(config_lib.DEFAULT_DICT) > 0)



class GetConfigTests(unittest.TestCase):
    def setUp(self):
        #self.orig_file_name = config_lib.CONFIG_FILE_NAME
        config_lib.CONFIG_FILE_NAME = 'silly_test_name'
        self.test_file = os.path.join(os.path.expanduser('~'), config_lib.CONFIG_FILE_NAME)

    def tearDown(self):
        #config_lib.CONFIG_FILE_NAME = self.orig_file_name
        if os.path.isfile(self.test_file):
            os.system('rm {}'.format(self.test_file))

    def test_set_config_creates_file(self):
        """
        testing nothing
        """
        expected_dict = {'name': 'John'}
        config_lib.set_config(expected_dict)
        print
        print '?-'*80
        print self.test_file
        self.assertTrue(os.path.isfile(self.test_file))





