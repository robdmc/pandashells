#! /usr/bin/env python

try:
    import pandas as pd
    import numpy as np
# will catch import errors in module_checker_lib so won't test this branch
except ImportError:  # pragma: nocover
    pass


def _next_power_two(x):
    """ given a number, returns the next power of two
    """
    x = int(x)
    n = 1
    while n < x:
        n = n << 1
    return n


def _compute_pad(t, interp_exponent=0):
    """
    Given a sorted time series t, compute the zero padding.
    The final padded arrays are the next power of two in length multiplied
    by 2 ** interp_exponent.
    returns t_pad and y_pad
    """
    t_min, t_max, n = t[0], t[-1], len(t)
    dt = (t_max - t_min) / float(n - 1)
    n_padded = _next_power_two(len(t)) << interp_exponent
    n_pad = n_padded - n
    t_pad = np.linspace(t_max + dt, t_max + dt + (n_pad - 1) * dt, n_pad)
    y_pad = np.zeros(len(t_pad))
    return t_pad, y_pad


def _compute_params(t):
    """
    Takes a timeseries and computes the parameters needed for the fast
    lomb scargle algorithm in gatspy
    """
    t_min, t_max, n = t[0], t[-1], len(t)
    dt = (t_max - t_min) / float(n - 1)
    min_freq = 1. / (t_max - t_min)
    d_freq = 1. / (2 * dt * len(t))
    return min_freq, d_freq, len(t)


def lomb_scargle(df, time_col, val_col, interp_exponent=0, freq_order=False):
    """
    :type df: pandas.DataFrame
    :param df: An input dataframe

    :type time_col: str
    :param time_col: The column of the dataframe holding the timestamps

    :type val_col: str
    :param val_col: The column of the dataframe holding the observations

    :type interp_exp: int
    :param interp_exp: Interpolate the spectrum by this power of two

    :type freq_order: bool
    :param freq_order: If set to True spectrum is returned in frequency order
                       instead of period order (default=False)

    :rtype: Pandas DataFrame
    :returns: A dataframe with columns: period, freq, power, amplitude
    """
    # do imports here to avoid loading plot libraries when this
    # module is loaded in __init__.py
    # which then doesn't allow for doing matplotlib.use() later
    import gatspy

    # only care about timestamped values
    df = df[[time_col, val_col]].dropna()

    # standardize column names, remove mean from values, and sort by time
    df = df.rename(columns={time_col: 't', val_col: 'y'}).sort_values(by=['t'])
    df['y'] = df['y'] - df.y.mean()

    #  compute total energy in the time series
    E_in = np.sum((df.y * df.y))

    # appropriately zero-pad the timeseries before taking spectrum
    pre_pad_length = len(df)
    t_pad, y_pad = _compute_pad(df.t.values, interp_exponent=interp_exponent)
    if len(t_pad) > 0:
        df = df.append(
            pd.DataFrame({'t': t_pad, 'y': y_pad}), ignore_index=True)

    # fit the lombs scargle model to the time series
    model = gatspy.periodic.LombScargleFast()
    model.fit(df.t.values, df.y.values, 1)

    # compute params for getting results out of lomb scargle fit
    f0, df, N = _compute_params(df.t.values)
    f = f0 + df * np.arange(N)
    p = 1. / f

    # retrieve the lomb scarge fit and normalize for power / amplitude
    yf = model.score_frequency_grid(f0, df, N)
    yf_power = 2 * yf * E_in * len(yf) / float(pre_pad_length) ** 2
    yf_amp = np.sqrt(yf_power)

    # generate the output dataframe
    df = pd.DataFrame(
        {'freq': f, 'period': p, 'power': yf_power, 'amp': yf_amp}
    )[['period', 'freq', 'power', 'amp']]

    # order by period if desired
    if not freq_order:
        df = df.sort_values(by='period')
    return df
