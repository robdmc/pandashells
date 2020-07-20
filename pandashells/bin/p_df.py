#! /usr/bin/env python

# standard library imports
import argparse
from importlib import import_module
import textwrap
import warnings
import os  # noqa
import re  # noqa
import sys  # noqa
import datetime  # noqa

from pandashells.lib import module_checker_lib


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
    warnings.filterwarnings('ignore')
    names_shortcuts = [
        ('datetime', 'datetime'),
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

    # make sure required modules are installed
    module_checker_lib.check_for_modules([m for (m, s) in out])
    warnings.resetwarnings()

    return out


def execute(cmd, scope_entries=None, retval_name=None):
    scope = scope_entries if scope_entries else {}
    from dateutil.parser import parse
    scope['parse'] = parse
    for (module, shortcut) in get_modules_and_shortcuts(sys.argv):
        scope[shortcut] = import_module(module)
    exec(cmd, scope)
    return scope.get(retval_name, None)


# TODO: same as above
# This function is run in the integrations tests, but since it's being
# run from a system call, coverage doesn't know about it.  I'm
# labeling it as no_cover because it actually does get run.
def exec_plot_command(args, cmd, df):  # pragma: no cover
    from pandashells.lib import plot_lib
    plot_lib.set_plot_styling(args)
    execute(cmd, scope_entries={'df': df})
    plot_lib.refine_plot(args)
    plot_lib.show(args)


def framify(cmd, df):
    import pandas as pd
    if isinstance(df, pd.DataFrame):
        return df
    else:
        try:
            return pd.DataFrame(df)
        except ValueError:
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
        df = execute(cmd, scope_entries={'df': df}, retval_name='df')
        return df

    # if this is a plot command, execute it and quit
    elif needs_plots([cmd]):
        exec_plot_command(args, cmd, df)
        sys.exit(0)

    # if instead this is a command on the whole frame
    else:
        # put results of command in temp var
        cmd = 'df = {}'.format(cmd)
        df = execute(cmd, scope_entries={'df': df}, retval_name='df')

    # make sure df is still dataframe and return
    df = framify(cmd, df)
    return df


# TODO: same as above
# This function is run in the integrations tests, but since it's being
# run from a system call, coverage doesn't know about it.  I'm
# labeling it as no_cover because it actually does get run.
def main():  # pragma: no cover
    # read command line arguments
    msg = textwrap.dedent(
        """
        Enables pandas dataframe processing at the unix command line.

        This is the real workhorse of the pandashells toolkit.  It reads data
        from stdin as a dataframe, which is passed through any number of pandas
        operations provided on the command line.  Output is always to stdout.

        Each operation assumes data is in a dataframe named df.  Operations
        performed on this dataframe will overwrite the df variable with
        the results of that operation.  Special consideration is taken for
        assignments such as df['a'] = df.b + df.c.  These are understood
        to agument the input dataframe with a new column. By way of example,
        this command:
            p.df 'df.groupby(by="a").b.count()' 'df.reset_index()'
        is equivalent to the python expressions:
            df = df.groupby(by="a").b.count()
            df = df.reset_index()

        In addition to providing access to pandas dataframes, a number of
        modules are loaded into the namespace so as to be accessible from the
        command line.  These modules are:
            pd = pandas
            np = numpy
            scp = scipy
            pl = pylab
            parse = dateutil.parser.parse
            datetime = datetime
            re = re

        ** Important **
        When creating chains of dataframe operations (see examples), it is
        important to express your chain of operations before any options. This
        is because some options can take multiple arguments and the parser
        won't be able to properly decode your meaning.
        For example:
            cat file.csv | p.df 'df["x"] = df.y + 1' -o table noheader  # GOOD
            cat file.csv | p.df -o table noheader 'df["x"] = df.y + 1'  # BAD

        Input can be read in different formats as specified by the -i switch.
        The most common formats are csv and table (white-space-delimited).  In
        either of these formats, p.df can accomodate input data that either
        does or doesn not have a header row.  When no header row is indicated,
        The columns of the Dataframe will be labeled as c0, c1, ..., cN.

        Plotting methods invoked on a Dataframe generate no output, but
        create an interactive plot instead.  There are a number of plot
        specific options available at the command line that govern the details
        of how these plots are rendered (e.g. --xlim, --legend, etc).

        -----------------------------------------------------------------------
        Examples:

            * Print a csv file in nice tabular format
                p.example_data -d tips | p.df -o table | head

            * Print a csv file to json
                p.example_data -d tips | head | p.df -o json

            * Transform csv to json then to table
                p.example_data -d tips | head | p.df -o json \\
                | p.df -i json -o table

            * Select by row
                p.example_data -d tips \\
                | p.df 'df[df.sex=="Female"]' 'df[df.smoker=="Yes"]' -o table

            * Extract columns
                p.example_data -d tips \\
                | p.df 'df[["total_bill", "tip"]].head()' -o table

            * Perform grouped aggregations
                p.example_data -d tips | p.df \\
                'df.groupby(by=["sex", "smoker"]).tip.sum()' -o table index

            * Use pandas plotting methods
                p.example_data -d tips | p.df \\
                'df.groupby(by="day").total_bill.sum().plot(kind="barh")'\\
                --xlabel 'Dollars' --title 'Total Bills by Day'

            * Convert between tabular and csv format with/without header rows
                seq 10 | awk '{print $1, 2*$1}'\\
                | p.df --names a b -i table noheader | p.df -o table noheader

        -----------------------------------------------------------------------
        """
    )
    from pandashells.lib import arg_lib

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)
    arg_lib.add_args(parser, 'io_in', 'io_out', 'decorating')
    msg = (
        '(MUST come before any options) '
        '[statement ...] Statement(s) to execute. '
    )
    parser.add_argument(
        "statement", help=msg, nargs="*")
    args = parser.parse_args()

    get_modules_and_shortcuts(args.statement)
    from pandashells.lib import io_lib

    # get the input dataframe
    df = io_lib.df_from_input(args)

    # execute the statements in order
    # plot commands are terminal statements so will call sys.exit()
    for cmd in args.statement:
        df = process_command(args, cmd, df)

    # write the output
    io_lib.df_to_output(args, df)

if __name__ == '__main__':  # pragma: no cover
    main()
