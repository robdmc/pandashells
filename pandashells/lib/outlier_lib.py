#! /usr/bin/env python

# standard library imports
import os
import sys
import argparse
import re

from pandashells.lib import module_checker_lib

# import required dependencies
module_checker_lib.check_for_modules(['pandas', 'numpy'])

import pandas as pd
import numpy as np


# recursive edit a series
def sigma_edit_series(sigma_thresh, in_series, ref_series=None):
    if in_series.count() == 0:
        msg = "Error:  No non-NaN values from which to remove outliers"
        raise ValueError(msg)

    ref = ref_series if ref_series else in_series.mean()
    resid = in_series - ref
    std = resid.std()
    sigma_t = sigma_thresh * std
    outside = resid.abs() >= sigma_t
    if any(outside):
        in_series[outside] = np.NaN
        in_series = sigma_edit_series(sigma_thresh, in_series, ref_series)

    return in_series

def ensure_col_exists(df, col, df_name):
    if df and (col not in df.columns):
        msg = '\n\n{} does not have column {}\n\n'.format(df_name, col)
        raise ValueError(msg)


def sigma_edit_dataframe(sigma_thresh, columns, df, df_ref=None):
    for col in columns:
        ensure_col_exists(df, col, 'df')
        ensure_col_exists(df_ref, col, 'df_ref')
        ser = df[col_name]
        ref_ser = df_ref[col_name] if df_ref else None
        df[col] = sigma_edit_series(sigma_thresh, ser, ref_series=ref_ser)
    return df
