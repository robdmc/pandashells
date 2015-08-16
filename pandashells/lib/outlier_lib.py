#! /usr/bin/env python

# standard library imports
from collections import Counter

import pandas as pd
import numpy as np


# recursive edit a series
def sigma_edit_series(sigma_thresh, in_series, iter_counter=None, max_iter=20):
    iter_counter = Counter() if iter_counter is None else iter_counter

    if in_series.count() == 0:
        msg = "Error:  No non-NaN values from which to remove outliers"
        raise ValueError(msg)

    iter_counter.update('n')
    if iter_counter['n'] > max_iter:
        msg = "Error:  Max Number of iterations exceeded in sigma-editing"
        raise ValueError(msg)

    resid = in_series - in_series.mean()
    std = resid.std()
    sigma_t = sigma_thresh * std
    outside = resid.abs() >= sigma_t
    if any(outside):
        in_series.loc[outside] = np.NaN
        in_series = sigma_edit_series(
            sigma_thresh, in_series, iter_counter, max_iter)

    return in_series


def ensure_col_exists(df, col, df_name='dataframe'):
    if not df.empty and col not in list(df.columns):
        msg = 'in sigma_edit: {} does not have column {}'.format(
            df_name, repr(col))
        raise ValueError(msg)


def sigma_edit_dataframe(sigma_thresh, columns, df, max_iter=20):
    """
    :type sigma_thresh: float
    :param sigma_thresh: The sigma threshold

    :type columns: list
    :param columns: a list of columns to sigma edit

    :type df: pandas.DataFrame
    :param df: The dataframe with columns of data to sigma-edit

    :type max_iter: int
    :param max_iter: Cap the number of iteration at this number

    :rtype: Pandas DataFrame
    :returns: A dataframe with ouliers set to NaN
    """
    # disable the chained assignment warning because raises fale alarm
    pd.options.mode.chained_assignment = None

    for col in columns:
        ensure_col_exists(df, col, 'df')
        ser = df[col]
        df.loc[:, col] = sigma_edit_series(sigma_thresh, ser, max_iter=max_iter)
    return df
