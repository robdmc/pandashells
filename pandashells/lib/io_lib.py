#! /usr/bin/env python

# --- standard library imports
import os
import sys
import argparse
import re
import csv

from pandashells.lib import module_checker_lib, config_lib
module_checker_lib.check_for_modules(['pandas'])

import pandas as pd


def df_from_input(args, in_file=None):
    if in_file is None:
        in_file = sys.stdin
    # --- set default read options
    config_dict = config_lib.get_config()
    header = 'infer'
    names = None
    encoding = 'utf-8'
    sep_dict = {
        'csv': ',',
        'table': r'\s+'}

    # --- overwrite read options based on supplied arguments
    if 'csv' in args.input_options:
        sep = sep_dict['csv']
    elif 'table' in args.input_options:
        sep = sep_dict['table']
    else:
        sep = sep_dict[config_dict['io_input_type']]

    if hasattr(args, 'columns'):
        if args.columns:
            names = [s.strip() for s in args.columns]
            header = 0

    if 'noheader' in args.input_options:
        header = None

    # --- read the input data
    df = pd.read_csv(in_file, sep=sep, header=header, names=names,
                     encoding=encoding)

    # --- if no names and no neader, create column names
    if 'noheader' in args.input_options:
        if not names:
            names = ['c{}'.format(nn) for nn, cc in enumerate(df.columns)]
            df.columns = pd.Index(names)
    return df


# ============================================================================
def df_to_output(args, df):
    # --- write options
    header = False if 'noheader' in args.output_options else True
    encoding = 'utf-8'
    index = False
    if 'index' in args.output_options:
        index = True
    config_dict = config_lib.get_config()

    # --- set table type to default if not specified
    if not set(args.output_options).intersection(['table', 'csv']):
        args.output_options.append(config_dict['io_output_type'])

    try:
        # --- print the data frame in the correct format
        if 'csv' in args.output_options:
            df.to_csv(sys.stdout, header=header, encoding=encoding,
                      quoting=csv.QUOTE_NONNUMERIC, index=index)
        elif 'table' in args.output_options:
            print df.to_string(header=header, index=index)
        elif 'html' in args.output_options:
            outString = "<style> table.dataframe "
            outString += "{border-width:1px; border-style:solid; "
            outString += "border-collapse:collapse; border-color: "
            outString += "LightGray;} </style>"
            outString += df.to_html(header=header, index=index)
            print outString
        else:
            msg = "\n\nOutput format must specify either 'csv' or 'table'"
            msg += " or 'html'"
            raise Exception(msg)
    except IOError:
        pass
