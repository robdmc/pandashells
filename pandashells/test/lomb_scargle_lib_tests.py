#! /usr/bin/env python

from unittest import TestCase
import pandas as pd
import numpy as np

from pandashells.lib.lomb_scargle_lib import (
    _next_power_two,
    _compute_pad,
    _compute_params,
    lomb_scargle,
)


class NextPowerTwoTest(TestCase):
    def test_proper_return(self):
        past_100 = _next_power_two(100)
        past_1000 = _next_power_two(1000)
        self.assertEqual(past_100, 128)
        self.assertEqual(past_1000, 1024)


class ComputePadTest(TestCase):
    def test_exp0(self):
        t = np.linspace(0, 10, 101)
        t_pad, y_pad = _compute_pad(t)
        dt = np.diff(t_pad)[-1]
        self.assertAlmostEqual(dt, 0.1)
        self.assertEqual(len(t_pad) + len(t), 128)
        self.assertEqual(set(y_pad), {0.})

    def test_exp2(self):
        t = np.linspace(0, 10, 101)
        t_pad, y_pad = _compute_pad(t, interp_exponent=2)
        dt = np.diff(t_pad)[-1]
        self.assertAlmostEqual(dt, 0.1)
        self.assertEqual(len(t_pad) + len(t), 512)
        self.assertEqual(set(y_pad), {0.})


class ComputeParamsTest(TestCase):
    def test_proper_return(self):
        t = np.linspace(0, 10, 101)
        min_freq, d_freq, N = _compute_params(t)
        self.assertAlmostEqual(min_freq, .1)
        self.assertAlmostEqual(d_freq, 0.049504950495)
        self.assertAlmostEqual(N, 101)


class LombScargleTest(TestCase):
    def test_no_pad(self):
        t = np.linspace(0, 10, 256)
        y = 7 * np.sin(2 * np.pi * t)
        df_in = pd.DataFrame({'t': t, 'y': y})
        df = lomb_scargle(df_in, 't', 'y')
        max_rec = df[df.amp == df.amp.max()].iloc[0]
        self.assertTrue(all([x > 0 for x in df.period.diff().dropna()]))
        self.assertAlmostEqual(max_rec['amp'], 7, places=0)
        self.assertAlmostEqual(max_rec['power'], 49, places=0)
        self.assertAlmostEqual(max_rec['period'], 1, places=0)
        self.assertAlmostEqual(max_rec['freq'], 1, places=0)
        self.assertEqual(len(df), 256)

    def test_with_pad(self):
        t = np.linspace(0, 10, 256)
        y = 7 * np.sin(2 * np.pi * t)
        df_in = pd.DataFrame({'t': t, 'y': y})
        df = lomb_scargle(df_in, 't', 'y', interp_exponent=1)
        max_rec = df[df.amp == df.amp.max()].iloc[0]
        self.assertTrue(all([x > 0 for x in df.period.diff().dropna()]))
        self.assertAlmostEqual(max_rec['amp'], 7, places=0)
        self.assertAlmostEqual(max_rec['power'], 49, places=0)
        self.assertAlmostEqual(max_rec['period'], 1, places=0)
        self.assertAlmostEqual(max_rec['freq'], 1, places=0)
        self.assertEqual(len(df), 512)

    def test_freq_order(self):
        t = np.linspace(0, 10, 256)
        y = 7 * np.sin(2 * np.pi * t)
        df_in = pd.DataFrame({'t': t, 'y': y})
        df = lomb_scargle(df_in, 't', 'y', freq_order=True)
        max_rec = df[df.amp == df.amp.max()].iloc[0]
        self.assertTrue(all([x > 0 for x in df.freq.diff().dropna()]))
        self.assertAlmostEqual(max_rec['amp'], 7, places=0)
        self.assertAlmostEqual(max_rec['power'], 49, places=0)
        self.assertAlmostEqual(max_rec['period'], 1, places=0)
        self.assertAlmostEqual(max_rec['freq'], 1, places=0)
        self.assertEqual(len(df), 256)
