#! /usr/bin/env python
import os
import json
from unittest import TestCase
from pandashells.lib import config_lib


class GlobalArgTests(TestCase):
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


class GetConfigTests(TestCase):
    def setUp(self):
        if os.path.isfile(config_lib.CONFIG_FILE_NAME):
            os.system('cp {f} {f}_orig'.format(f=config_lib.CONFIG_FILE_NAME))

    def tearDown(self):
        if os.path.isfile(config_lib.CONFIG_FILE_NAME + '_orig'):
            os.system('mv {f}_orig {f}'.format(f=config_lib.CONFIG_FILE_NAME))
        else:  # pragma: no cover
            os.system('rm  {f}'.format(f=config_lib.CONFIG_FILE_NAME))

    def test_set_config_creates_file(self):
        """
        set_config() function writes to file
        """
        expected_dict = {'name': 'John'}
        config_lib.set_config(expected_dict)
        with open(config_lib.CONFIG_FILE_NAME) as jsonfile:
            saved_dict = json.loads(jsonfile.read())
        self.assertEqual(expected_dict, saved_dict)

    def test_get_config_non_existent_file(self):
        """
        get_config() creates config file when it doesn't exist
        """
        if os.path.isfile(config_lib.CONFIG_FILE_NAME):
            os.system('rm {}'.format(config_lib.CONFIG_FILE_NAME))
        config = config_lib.get_config()
        self.assertEqual(config_lib.DEFAULT_DICT, config)

    def test_get_config_existing_file(self):
        """
        get_config() reads existing file
        """
        if os.path.isfile(config_lib.CONFIG_FILE_NAME):
            os.system('rm {}'.format(config_lib.CONFIG_FILE_NAME))

        test_config = {'name': 'Bill'}
        with open(config_lib.CONFIG_FILE_NAME, 'w') as f:
            f.write(json.dumps(test_config))
        config = config_lib.get_config()
        self.assertEqual(test_config, config)
