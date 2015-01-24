#! /usr/bin/env python
import sys
import importlib

# --- define the default error message to show when a module can't be found
HEADER = "\n\nThis tool requires packages that have not been installed.\n"
HEADER += "Below is a list of missing packages along with commands for\n"
HEADER += "installing them.\n\n"

# --- define a dict to map a module name to its install command
CMD_DICT = {
    'dateutil': 'pip install dateutil',
    'matplotlib': 'conda install matplotlib',
    'mpld3': 'mpld3',
    'numpy': 'conda install numpy',
    'pandas': 'pip install pandas',
    'pylab': 'conda install matplotlib',
    'requests': 'pip install requests',
    'scipy': 'conda install scipy',
    'seaborn': 'pip install seaborn',
    'statsmodels': 'pip install statsmodels',
}


# ============================================================================
def check_for_modules(module_list):
    # --- make sure module_list only contains recognized modules
    unnamed_modules = set(module_list) - set(CMD_DICT.keys())
    if unnamed_modules:
        msg = '\n\nThese modules unrecognized by check_for_modules(): '
        msg += '{}\n'.format(unnamed_modules)
        raise ValueError(msg)

    # --- initialize an error message
    msg = ''

    # --- try importing all the required mojkdules
    for module in module_list:
        try:
            importlib.import_module(module)
        except ImportError:
            # --- add to error message for each bad module
            msg = msg if msg else HEADER
            msg += '-'*60 + '\n'
            msg += "Missing module '{}'. To install use: \n".format(module)
            msg += "    {}\n\n".format(CMD_DICT[module])

    # --- raise value error with message if bad modules found
    if msg:
        raise ImportError(msg)
