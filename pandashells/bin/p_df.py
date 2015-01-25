#! /usr/bin/env python

# standard library imports
import argparse
import datetime
import importlib
import os
import re
import sys

from pandashells.lib import module_checker_lib, arg_lib, io_lib

# Note:
# There are some conditional imports into global scope 
# right after the first two functions


def needs_plots(command_list):
    # define regex to identify plot commands
    plot_command_list = [
        'plot', 'hist', 'scatter', 'figure', 'subplot', 'xlabel', 'ylabel',
        'set_xlabel', 'set_ylabel', 'title', 'set_xlim', 'set_ylim', 'legend',
        'twinx', 'gca', 'gcf'
    ]
    rex_plot_str = r'.*({})\(.*\).*'.format('|'.join(plot_command_list))
    if re.compile(rex_plot_str).match(' '.join(command_list)):
        return True
    else:
        return False

def get_modules_and_shortcuts(command_list):
    names_shortcuts = [
        ('numpy', 'np'),
        ('scipy', 'scp'),
        ('pylab', 'pl'),
        ('seaborn', 'sns'),
    ]
    base_requirements = [
        ('pandas', 'pd'),
        ('dateutil', 'dateutil'),
    ]
    out = base_requirements + [
        tup for tup in names_shortcuts
        if '{}.'.format(tup[1]) in ' '.join(command_list)
    ]
    if needs_plots(command_list):
        out = list(set([('pylab', 'pl')] + out))
    return out

# make sure all the required modules are installed
module_checker_lib.check_for_modules([
    m for (m, s) in get_modules_and_shortcuts(sys.argv)
])

# import required modules into the global scope
import pandas as pd
from dateutil.parser import parse
for (module, shortcut) in get_modules_and_shortcuts(sys.argv):
    exec('import {} as {}'.format(module, shortcut))
if needs_plots(sys.argv):
    from pandashells.lib import plot_lib


def exec_plot_command(args, cmd, df):
    plot_lib.set_plot_styling(args)
    exec(cmd)
    plot_lib.refine_plot(args)
    plot_lib.show(args)

def framify(cmd, df):
    if isinstance(df, pd.DataFrame):
        return df
    else:
        try:
            return pd.DataFrame(df)
        except pd.core.common.PandasError:
            msg = (
                '\n\nResult of command: \n'
                '\'{cmd}\' \n'
                'could not be cast to dataframe\n\n'
            ).format(cmd=cmd)
            sys.stderr.write(msg)
            sys.exit(1)


def process_command(args, cmd, df):
    # define regex to identify if supplied command is for col assignment
    rex_col_cmd = re.compile(r'.*?df\[.+\].*?=')

    # if this is a column-assignment command, just execute it
    if rex_col_cmd.match(cmd):
        'matches col'
        exec(cmd)
        return df

    # if this is a plot command, execute it and quit
    elif needs_plots([cmd]):
        exec_plot_command(args, cmd, df)
        sys.exit(0)

    # if instead this is a command on the whole frame
    else:
        # put results of command in temp var
        cmd = 'df = {}'.format(cmd)
        exec(cmd)

    # make sure df is still dataframe and return
    df = framify(cmd, df)
    return df

def main():
    # read command line arguments
    msg = (
        "Bring pandas manipulation to command line.  Input from stdin "
         "is placed into a dataframe named 'df'.  The output of each "
         "command must evaluate to either a dataframe or a series."
         "The output of each command will be available to the next command "
         "as 'df'. The output of the final command will be sent "
         "to stdout.  The namespace in which the commands are executed "
         "includes pandas as pd, numpy as np, scipy as scp, pylab as pl, "
         "dateutil.parser.parse as parse, datetime.  Plot-specific "
         "commands will be ignored unless a supplied command creates "
         "a plot. "
    )
    parser = argparse.ArgumentParser(description=msg)
    arg_lib.add_args(parser, 'io_in', 'io_out', 'decorating', 'example')
    parser.add_argument(
        "statement", help="[statement ...] Statement(s) to execute", nargs="*")
    args = parser.parse_args()

    # get a list of commands to execute
    command_list = args.statement

    # get the input dataframe
    df = io_lib.df_from_input(args)

    # execute the statements in order 
    # plot commands are terminal statements so will call sys.exit()
    for cmd in args.statement:
        df = process_command(args, cmd, df)

    # write the output
    io_lib.df_to_output(args, df)

if __name__ == '__main__': # pragma: no cover
    main()
