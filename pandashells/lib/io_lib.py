#! /usr/bin/env python

#--- standard library imports
import os
import sys
import argparse
import re
import csv

############# dev only.  Comment out for production ######################
sys.path.append('../..')
##########################################################################


from pandashells.lib import module_checker_lib

#--- import required dependencies
modulesOkay = module_checker_lib.check_for_modules(
        [
            'pandas',
        ])
if not modulesOkay:
    sys.exit(1)

import pandas as pd

#=============================================================================
def df_from_input(args, in_file=None):
    if in_file is None:
        in_file = sys.stdin
    #--- set default read options
    sep = None
    header = 'infer'
    names = None
    encoding='utf-8'

    #--- overwrite read options based on supplied arguments
    if 'csv' in args.input_options[0]:
        sep = ','
    if 'table' in args.input_options[0]:
        sep = r'\s+'
    if 'noheader' in args.input_options[0]:
        header = None

    if hasattr(args, 'columns'):
        if args.columns:
            names = [s.strip() for s in args.columns[0].split(',')]
            header = None

    #--- read the input data
    df = pd.read_csv(in_file, sep=sep, header=header, names=names,
            encoding=encoding)
    return df

#=============================================================================
def df_to_output(args, df):
    #--- write options
    header = False if 'noheader' in args.output_options[0] else True
    encoding='utf-8'
    index = False
    if 'index' in args.output_options[0]:
        if  not 'noindex' in args.output_options[0]:
            index = True

    try:
        #--- print the data frame in the correct format
        if 'csv' in args.output_options[0]:
            df.to_csv(sys.stdout, header=header, encoding=encoding,
                    quoting=csv.QUOTE_NONNUMERIC, index=index)
        elif 'table' in args.output_options[0]:
            print df.to_string(header=header, index=index)
        elif 'html' in args.output_options[0]:
            outString = "<style> table.dataframe { border-width:1px; border-style:solid; border-collapse:collapse; border-color: LightGray; } </style>"
            outString += df.to_html(header=header, index=index)
            print outString
        else:
            msg = "\n\nOutput format must specify either 'csv' or 'table'"
            msg += " or 'html'"
            raise Exception(msg)
    except IOError:
        pass
