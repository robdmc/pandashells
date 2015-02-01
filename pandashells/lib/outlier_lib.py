#! /usr/bin/env python

# standard library imports
from collections import Counter
import argparse
import os
import re
import sys

from pandashells.lib import module_checker_lib

# import required dependencies
module_checker_lib.check_for_modules(['pandas', 'numpy'])

import pandas as pd
import numpy as np

# disable the chained assignment warning because raises fale alarm
pd.options.mode.chained_assignment = None

# recursive edit a series
def sigma_edit_series(
        sigma_thresh, in_series,
        ref_series=None, iter_counter=None, max_iter=20):
    iter_counter = Counter() if iter_counter is None else iter_counter

    if in_series.count() == 0:
        msg = "Error:  No non-NaN values from which to remove outliers"
        raise ValueError(msg)

    iter_counter.update('n')
    if iter_counter['n'] > max_iter:
        msg = "Error:  Max Number of iterations exceeded in sigma-editing"
        raise ValueError(msg)

    ref = in_series.mean() if ref_series is None else ref_series
    resid = in_series - ref
    std = resid.std()
    sigma_t = sigma_thresh * std
    outside = resid.abs() >= sigma_t
    if any(outside):
        in_series.loc[outside] = np.NaN
        in_series = sigma_edit_series(sigma_thresh, in_series,
            ref_series, iter_counter, max_iter)

    return in_series

def ensure_col_exists(df, col, df_name='dataframe'):
    if not df.empty and col not in list(df.columns):
        msg = 'in sigma_edit: {} does not have column {}'.format(df_name, repr(col))
        raise ValueError(msg)


def sigma_edit_dataframe(sigma_thresh, columns, df, ref_ser=None):
    for col in columns:
        ensure_col_exists(df, col, 'df')
        ser = df[col]
        df.loc[:, col] = sigma_edit_series(sigma_thresh, ser, ref_series=ref_ser)
    return df
