#! /usr/bin/env python

from collections import Counter
import warnings
import sys
import importlib
from pandashells.lib import config_lib

# define the default error message to show when a module can't be found
HEADER = "\n\nThis tool requires packages that have not been installed.\n"
HEADER += "Below is a list of missing packages along with commands for\n"
HEADER += "installing them.\n\n"

# define a dict to map a module name to its install command
CMD_DICT = {
    'dateutil': 'pip install dateutil',
    'gatspy': 'pip install gatspy',
    'matplotlib': 'pip install matplotlib',
    'mpld3': 'pip install mpld3',
    'numpy': 'pip install numpy',
    'pandas': 'pip install pandas',
    'pandasgui': 'pip install pandasgui',
    'pylab': 'pip install matplotlib',
    'requests': 'pip install requests',
    'scipy': 'pip install scipy',
    'seaborn': 'pip install seaborn',
    'statsmodels': 'pip install statsmodels',
    'supersmoother': 'pip install supersmoother',
}

BACKEND_COUNTER = Counter()


def set_backend():
    with warnings.catch_warnings():
        if BACKEND_COUNTER['use_called'] == 0:
            try:
                warnings.filterwarnings('ignore')
                import matplotlib
                config = config_lib.get_config()
                matplotlib.use(config['plot_backend'])
                BACKEND_COUNTER.update({'use_called': 1})
                warnings.resetwarnings()
            except ImportError:  # pragma nocover
                pass


def check_for_modules(module_list):
    # make sure module_list only contains recognized modules
    unnamed_modules = set(module_list) - set(CMD_DICT.keys())
    unnamed_modules = unnamed_modules - {'datetime', 're'}
    if unnamed_modules:
        msg = '\n\nThese modules unrecognized by check_for_modules(): '
        msg += '{}\n'.format(unnamed_modules)
        raise ValueError(msg)

    # try using configured backend ignoring errors so they'll be caught later
    if set(module_list).intersection({'matplotlib', 'pylab', 'seaborn'}):
        set_backend()

    # initialize an error message
    msg = ''

    # try importing all the required mojkdules
    for module in sorted(module_list):
        try:
            importlib.import_module(module)
        except ImportError:
            # add to error message for each bad module
            msg = msg if msg else HEADER
            msg += '-' * 60 + '\n'
            msg += "Missing module '{}'. To install use: \n".format(module)
            msg += "    {}\n\n".format(CMD_DICT[module])
    if msg:
        sys.stdout.write(msg + '\n')
        sys.exit(1)
