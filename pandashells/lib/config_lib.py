#! /usr/bin/env python
import os
import json

# the name of the file in which to store configuration
CONFIG_FILE_NAME = '.pandashells'

# valid options  (option_name, [valid, option, list])
CONFIG_OPTS = sorted(
    [
        ('io_input_type', ['csv', 'table']),
        ('io_output_type', ['csv', 'table', 'html']),
        ('io_input_header', ['header', 'noheader']),
        ('io_output_header', ['header', 'noheader']),
        ('io_output_index', ['noindex', 'index']),
        ('io_output_na_rep', ['nan', 'NaN', '', '-']),
        ('plot_context', ['talk', 'poster', 'paper', 'notebook']),
        ('plot_theme', ['darkgrid', 'whitegrid', 'dark', 'white']),
        ('plot_palette', ['muted', 'deep', 'dark', 'colorblind', 'pastel']),
        ('plot_backend', [
            'TkAgg',
            'WebAgg',
            'macosx',
            'Qt5Agg',
            'GTKAgg',
            'GTK3Agg',
            'GTK',
            'GTKCairo',
            'GTK3Cairo',
            'WXAgg',
            'WX',
            'Qt4Agg',
        ]),
    ]
)

# create a dictionary out of the config options
DEFAULT_DICT = {t[0]: t[1][0] for t in CONFIG_OPTS}

# compute the full path to the config file
HOME = os.path.expanduser('~')
CONFIG_FILE_NAME = os.path.join(HOME, CONFIG_FILE_NAME)


def set_config(config_dict):
    """Persists the supplied configuration dictionary to disk

    :type config_dict: dict
    :param config_dict: A dictionary of configuration options
    """
    with open(CONFIG_FILE_NAME, 'w') as config_file:
        config_file.write(json.dumps(config_dict, indent=2))


def get_config():
    """Get the current configuration options

    Will create and persist a set of default options if they don't exist.

    :rtype: dict
    :returns: A dictionary of configuration options
    """
    if os.path.isfile(CONFIG_FILE_NAME):
        with open(CONFIG_FILE_NAME, 'r') as config_file:
            config_dict = json.loads(config_file.read())
    else:
        config_dict = DEFAULT_DICT
        set_config(config_dict)
    return config_dict
