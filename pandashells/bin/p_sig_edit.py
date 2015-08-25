#! /usr/bin/env python

# standard library imports
import argparse
import textwrap

from pandashells.lib import arg_lib, module_checker_lib
module_checker_lib.check_for_modules(['pandas'])
from pandashells.lib import io_lib, outlier_lib


def main():
    msg = textwrap.dedent(
        """
        Remove outliers from DataFrame columns using a recursive sigma-edit
        algorithm.  The algorithm will recursively NaN out values greater than
        sigma_thresh standard deviations away from sample mean.

        -----------------------------------------------------------------------
        Examples:

            * Do a 2.5-sigma edit on a gamma distribution and show histogram
                p.rand -n 1000 -t gamma --alpha=3 --beta=.01\\
                | p.df 'df["c1"] = df.c0'\\
                | p.sig_edit -c c1 -t 2.5\\
                | p.df 'pd.melt(df)' --names raw edited\\
                | p.facet_grid --hue variable --map pl.hist\\
                   --args value --kwargs 'alpha=.2' 'range=[0, 1000]' 'bins=50'
        -----------------------------------------------------------------------
        """
    )

    #  read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    arg_lib.add_args(parser, 'io_in', 'io_out')

    parser.add_argument("-t", "--sigma_thresh", help="Sigma threshold",
                        nargs=1, required=True, type=float)
    parser.add_argument("-c", "--cols", required=True,
                        help="Column(s) to sigma-edit", nargs="+")
    parser.add_argument("--max_iter", help="Max number of recursions",
                        nargs=1, type=int, default=[20])

    # parse arguments
    args = parser.parse_args()

    # get the input dataframe
    df = io_lib.df_from_input(args)
    df = outlier_lib.sigma_edit_dataframe(
        args.sigma_thresh[0], args.cols, df, max_iter=args.max_iter[0])

    # write dataframe to output
    io_lib.df_to_output(args, df)

if __name__ == '__main__':  # pragma: no cover
    main()
