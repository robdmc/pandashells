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

ENCODING = 'utf-8'


def get_separator(args, config_dict):
    sep_dict = {'csv': ',', 'table': r'\s+'}
    input_type_set = set(args.input_options).intersection(set(sep_dict.keys()))
    if input_type_set:
        input_type = list(input_type_set)[0]
    else:
        input_type = config_dict['io_input_type']
    return sep_dict[input_type]


def get_header_names(args):
    if hasattr(args, 'names') and args.names:
        header = 0
        names = [s.strip() for s in args.names]
    else:
        header, names = 'infer',  None

    if 'noheader' in args.input_options:
        header = None
    return header, names

def get_nan_rep(args, config_dict):
    OKAY HERES THE DEAL.  I WAS WORKING P.SIG_EDIT WHEN I REALIZED
    I WANTED TO SPECIFY NAN_REP ON IO_LIB.  HENCE THIS FUNCTION.
    I AM NOW IN A PLACE WHERE I NEED TO ADD NAN_REP STUFF TO ARGLIB
    IN ORDER TO MAKE THIS WORK.

    NOTE THAT THIS WORK IS HAPPENING IN THE P_CONFIG_TESTS BRANCH
    WHICH SHOULD GET MERGED INTO THE P_SIG_EDIT_TESTS BRANCH
    WHICH THEN CAN GET MERGED INTO THE ADD_TESTS BRANCH.
    if hasattr(args, 
    sep_dict = {'csv': ',', 'table': r'\s+'}
    input_type_set = set(args.input_options).intersection(set(sep_dict.keys()))
    if input_type_set:
        input_type = list(input_type_set)[0]
    else:
        input_type = config_dict['io_input_type']
    return sep_dict[input_type]

def df_from_input(args, in_file=None):
    # --- set up proper state for reading input
    config_dict = config_lib.get_config()
    in_file = sys.stdin if in_file is None else in_file
    sep = get_separator(args, config_dict)
    header, names = get_header_names(args)

    # --- read the input data
    df = pd.read_csv(in_file, sep=sep, header=header, names=names,
                     encoding=ENCODING)

    # --- if no names and no neader, create column names
    if ('noheader' in args.input_options) and (not names):
        names = ['c{}'.format(nn) for nn, cc in enumerate(df.columns)]
        df.columns = pd.Index(names)
    return df


def csv_writer(df, header, index):
    df.to_csv(sys.stdout, header=header, encoding=ENCODING,
              quoting=csv.QUOTE_NONNUMERIC, index=index)


def table_writer(df, header, index):
    sys.stdout.write(df.to_string(header=header, index=index) + '\n')


def html_writer(df, header, index):
    outString = "<style> table.dataframe "
    outString += "{border-width:1px; border-style:solid; "
    outString += "border-collapse:collapse; border-color: "
    outString += "LightGray;} </style>"
    outString += df.to_html(header=header, index=index)
    sys.stdout.write(outString + '\n')


def df_to_output(args, df):
    # --- set up write options
    config_dict = config_lib.get_config()
    header = False if 'noheader' in args.output_options else True
    index = True if 'index' in args.output_options else False

    # --- define valid output types
    valid_outputs = [
        'table',
        'csv',
        'html',
    ]

    # --- get the output type
    output_type_set = set(args.output_options).intersection(set(valid_outputs))
    if output_type_set:
        output_type = list(output_type_set)[0]
    else:
        output_type = config_dict['io_output_type']

    # --- set up a mapping between output type and writer function
    writer_for = {
        'csv': csv_writer,
        'table': table_writer,
        'html': html_writer,
    }

    # --- call writer in try block to gracefully handle closed pipes
    try:
        writer_for[output_type](df, header, index)
    except IOError:
        pass
