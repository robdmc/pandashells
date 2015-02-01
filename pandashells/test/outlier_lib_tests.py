#! /usr/bin/env python
import argparse
import copy
import json
import os
import sys
import StringIO
import subprocess
import tempfile


from mock import patch, MagicMock, call
from unittest import TestCase
import pandas as pd
import numpy as np

from pandashells.lib import arg_lib, config_lib
import pandashells.bin.p_df
from pandashells.lib.outlier_lib import (
    sigma_edit_series,
    ensure_col_exists,
)


def all_in_bounds(sigma_thresh, ser, ref=None):
    ref = ser.mean() if ref is None else ref
    abs_resid = (ser - ref).dropna().abs()
    bound = sigma_thresh * ser.std()
    return all(abs_resid < bound)



class SigmaEditSeriesTests(TestCase):
    def test_empty_series(self):
        sigma_thresh = 3
        ser = pd.Series([])

        with self.assertRaises(ValueError):
            sigma_edit_series(sigma_thresh, ser, ref_series=None)

    def test_nan_series(self):
        sigma_thresh = 3
        ser = pd.Series([np.NaN for nn in range(10)])

        with self.assertRaises(ValueError):
            sigma_edit_series(sigma_thresh, ser, ref_series=None)

    def test_nothing_removed(self):
        sigma_thresh = 10
        ser = pd.Series([1, 2, 3, 4, 5])
        ser = sigma_edit_series(sigma_thresh, ser, ref_series=None, max_iter=1)
        self.assertEqual(list(ser), [1, 2 , 3 , 4, 5])

    def test_two_pass(self):
        sigma_thresh = 2
        ser = pd.Series([-4] + [0, 1, 2] * 4 + [ 5])
        ser = sigma_edit_series(sigma_thresh, ser, ref_series=None, max_iter=2)
        self.assertTrue(all_in_bounds(sigma_thresh, ser, ref=None))

    def test_two_pass_exceed_iter(self):
        sigma_thresh = 2
        ser = pd.Series([-4] + [0, 1, 2] * 4 + [ 5])
        with self.assertRaises(ValueError):
            ser = sigma_edit_series(
                sigma_thresh, ser, ref_series=None, max_iter=1)

    def test_three_pass(self):
        sigma_thresh = 2
        ser = pd.Series([-4, -4] + [0, 1, 2] * 4 + [5,])
        ser = sigma_edit_series(sigma_thresh, ser, ref_series=None, max_iter=3)
        self.assertTrue(all_in_bounds(sigma_thresh, ser, ref=None))

    def test_three_pass_with_ref(self):
        sigma_thresh = 2
        ser = pd.Series([-4, -4] + [0, 1, 2] * 4 + [5,])
        ref = pd.Series(range(len(ser)))
        ser = ser - ser.mean()+ ref
        ser = sigma_edit_series(sigma_thresh, ser, ref_series=ref, max_iter=3)
        self.assertTrue(all_in_bounds(sigma_thresh, ser, ref=ref))


class EnsureColExistsTests(TestCase):
    def test_col_exists(self):
        df = pd.DataFrame({'a': [1, 2, 3]})
        ensure_col_exists(df, 'a')

    def test_col_does_not_exist(self):
        df = pd.DataFrame({'a': [1, 2, 3]})
        with self.assertRaises(ValueError):
            ensure_col_exists(df, 'b', 'my_df')
