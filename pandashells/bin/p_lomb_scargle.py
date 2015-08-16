#! /usr/bin/env python

# standard library imports
import argparse
import textwrap
import sys  # noqa

from pandashells.lib import arg_lib, module_checker_lib
module_checker_lib.check_for_modules(['pandas', 'gatspy'])

from pandashells.lib import io_lib, lomb_scargle_lib


def main():
    msg = textwrap.dedent(
        """
        Computes a spectrogram using the lomb-scargle algorithm provided by
        the gatspy module.  The input time series need not have evenly spaced
        time-stamps.  The FFT-based algorithm has complexity O[N*log(N)].

        -----------------------------------------------------------------------
        Examples:

            * Plot the spectrum of a simple sine wave
                  p.linspace 0 10 100 \\
                  | p.df 'df["value"] = 7 * np.sin(2*np.pi*df.time / 1.5)'\\
                        --names time\\
                  | p.lomb_scargle -t time -y value --interp_exp 3\\
                  | p.plot -x period -y amp --xlim 0 3

            * Show the annual and 59-day peaks in the sealevel spectrum
                p.example_data -d sealevel\\
                | p.df 'df["day"] = 365.25 * df.year'\\
                        'df["day"] = df.day - df.day.iloc[0]'\\
                | p.lomb_scargle -t day -y sealevel_mm --interp_exp 3\\
                | p.df 'df[df.period < 720]'\\
                | p.plot -x period -y amp --xlim 1 400\\
                         --title 'Sea-surface height spectrum'\\
                         --xlabel 'period (days)'

        -----------------------------------------------------------------------
        """
    )

    # read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    arg_lib.add_args(parser, 'io_in', 'io_out')

    parser.add_argument('-t', '--time_col', help='Time Column',
                        nargs=1, required=True, type=str)

    parser.add_argument('-y', '--observation_col', help='Observation column',
                        nargs=1, dest='val_col', required=True, type=str)

    parser.add_argument('--interp_exp', help='Interpolate by this power of 2',
                        nargs=1, type=int, default=[1])
    parser.add_argument(
        '--freq_order', action='store_true', dest='freq_order', default=False,
        help='Order output by freqency instead of period')

    # parse arguments
    args = parser.parse_args()

    # get the input dataframe
    df = io_lib.df_from_input(args)
    df = lomb_scargle_lib.lomb_scargle(
        df, args.time_col[0], args.val_col[0], args.interp_exp[0],
        args.freq_order)

    # write dataframe to output
    io_lib.df_to_output(args, df)

if __name__ == '__main__':  # pragma: no cover
    main()
