#! /usr/bin/env python
import sys
import importlib

# --- define the default error message to show when a module can't be found
HEADER = "\n\nThis tool has missing dependencies.  Below is a list of \n"
HEADER += "the missing packages along with commands for installing them.\n"

# --- define a dict to map a module name to its install command
CMD_DICT = {
    'numpy': 'conda install numpy',
    'scipy': 'conda install scipy',
    'matplotlib': 'conda install matplotlib',
    'pandas': 'pip install pandas',
    'statsmodels': 'pip install statsmodels',
    'seaborn': 'pip install seaborn',
    'requests': 'pip install requests',
    'toolz': 'pip install toolz',
    'mpld3': 'mpld3'}


# ============================================================================
def check_for_modules(moduleList=[]):
    badModList = []
    # --- try importing all the required modules
    for module in moduleList:
        try:
            importlib.import_module(module)
        except ImportError:
            badModList.append(module)

    if badModList:
        sys.stderr.write(HEADER)
        for mod in badModList:
            msg = '-'*60 + '\n'
            msg += "Missing module '{}'. To install use: \n".format(mod)
            msg += "    {}\n".format(CMD_DICT[mod])
            msg += '\n\n'
            sys.stderr.write(msg)
        return False
    else:
        return True
