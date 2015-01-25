#! /usr/bin/env python

# standard library imports
import argparse
import datetime
import importlib
import os
import re
import sys

from pandashells.lib import module_checker_lib, arg_lib, io_lib


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


def exec_plot_command(args, cmd, df):
    exec(cmd)
    from pandashells.lib import plot_lib
    plot_lib.refine_plot(args)
    plot_lib.show(args)

def framify(cmd, df):
    import pandas as pd
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


def process_command(cmd, df):
        # define regex to identify if supplied command is for col assignment
        rex_col_cmd = re.compile(r'.*?df\[.+\].*?=')

        # if this is a column-assignment command, just execute it
        if rex_col_cmd.match(cmd):
            exec(cmd)
            return df

        # if this is a plot command, execute it and quit
        elif needs_plots(cmd):
            exec_plot_command(cmd, df)
            sys.exit()

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

    # make sure all the required modules are installed
    module_checker_lib.check_for_modules([
        m for (m, s) in get_modules_and_shortcuts(command_list)
    ])

    # import required modules
    from dateutil.parser import parse
    for (module, shortcut) in get_modules_and_shortcuts(command_list):
        exec('import {} as {}'.format(module, shortcut))

    # get the input dataframe
    df = io_lib.df_from_input(args)

    # execute the statements in order 
    # plot commands are terminal statements so will call sys.exit()
    for cmd in args.statement:
        df = process_command(cmd, df)

    # write the output
    io_lib.df_to_output(args, df)

if __name__ == '__main__':
    main()

#    # set up plot styling in case it's needed
#    plot_lib.set_plot_styling(args)
#
#
#
#
#    # execute the statements in sequence
#    for cmd in args.statement:
#        # if this is a column-assignment command, just execute it
#        if rex_col_cmd.match(cmd):
#            exec(cmd)
#            temp = df
#        # if this is a plot command, execute it and quit
#        elif rex_plot_cmd.match(cmd):
#            exec(cmd)
#            needs_show = True
#
#        # if instead this is a command on the whole frame
#        else:
#            # put results of command in temp var
#            cmd = 'temp = {}'.format(cmd)
#            exec(cmd)
#
#        # transform results to dataframe if needed
#        if not rex_plot_cmd.match(cmd):
#            if isinstance(temp, pd.DataFrame):
#                df = temp
#            else:
#                try:
#                    df = pd.DataFrame(temp)
#                except pd.core.common.PandasError:
#                    print temp
#                    sys.exit(0)
#
#    # show plots if requested
#    if needs_show:
#        plot_lib.refine_plot(args)
#        plot_lib.show(args)
#    # otherwise print results
#    else:
#        io_lib.df_to_output(args, df)
#
#
#
#
#
#
##class CommandProcessor(object):
##    def __init__(self, args):
##        self.args = args
##        # define regex to identify if supplied command is for col assignment
##        self.rex_col_cmd = re.compile(r'.*?df\[.+\].*?=')
##
##        # define regex to identify plot commands
##        plot_command_list = [
##            'plot', 'hist', 'scatter', 'figure', 'subplot', 'xlabel', 'ylabel',
##            'set_xlabel', 'set_ylabel', 'title', 'set_xlim', 'set_ylim',
##            'legend', 'twinx', 'gca', 'gcf'
##        ]
##        pstring = '|'.join(plot_command_list)
##        rex_plot_str = r'.*({})\(.*\).*'.format(pstring)
##        self.rex_plot_cmd = re.compile(rex_plot_str)
##
##        # read in the commands
##        self.command_list = args.statement
##
##        # read the input dataframe
##        self.df = io_lib.df_from_input(self.args)
##
##
##    def _
##
#
#
