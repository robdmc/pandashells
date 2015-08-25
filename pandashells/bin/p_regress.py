#! /usr/bin/env python

# standard library imports
import sys
import argparse
import textwrap
import importlib

from pandashells.lib import module_checker_lib, arg_lib

# import required dependencies
module_checker_lib.check_for_modules(['pandas', 'statsmodels', 'scipy'])


from pandashells.lib import io_lib
import scipy as scp  # NOQA
import statsmodels.formula.api as sm


# this silly function helps use side_effect in mocking tests
def get_module(name):  # pragma nocover
    return importlib.import_module(name)


def main():
    msg = textwrap.dedent(
        """
        Performs (multivariable) linear regression.  The fitting model
        is specified using the R-like, patsy syntax.  Input is from stdin
        and output is either fitting information or the input data
        with columns added for the fit and residuals.

        -----------------------------------------------------------------------
        Examples:
            * Fit a line to the sea-level data
                p.example_data -d sealevel | p.regress -m 'sealevel_mm ~ year'

            * Fit a trend plus annual cycle to sealevel data
                p.example_data -d sealevel \\
                | p.df 'df["sin"] =  np.sin(2 * np.pi * df.year)' \\
                | p.df 'df["cos"] = np.cos(2 * np.pi * df.year)' \\
                | p.regress -m 'sealevel_mm ~ year + cos + sin'

            * Examine residual ECDF of trend plus annual fit
                p.example_data -d sealevel \\
                | p.df 'df["sin"] =  np.sin(2 * np.pi * df.year)' \\
                | p.df 'df["cos"] = np.cos(2 * np.pi * df.year)' \\
                | p.regress -m 'sealevel_mm ~ year + cos + sin' --fit \\
                | p.cdf -c 'resid_' --title 'ECDF of trend + annual'

            * Detrend sealevel data to more clearly reveal oscillations
                p.example_data -d sealevel \\
                | p.regress -m 'sealevel_mm ~ year' --fit \\
                | p.plot -x year -y resid_ --ylabel 'Trend removed (mm)' \\
                         --title 'Global Sea Surface Height'

            * Set origin of sealevel data to 0 and regress with no intercept
                p.example_data -d sealevel\\
                | p.df 'df["year"] = df.year - df.year.iloc[0]'\\
                'df["sealevel_mm"] = df.sealevel_mm - df.sealevel_mm.iloc[0]'\\
                | p.regress -m 'sealevel_mm ~ year - 1' --fit\\
                | p.plot -x year -y sealevel_mm fit_ --style '.' '-'\\
                     --alpha .2 1 --legend best --title 'Force Zero Intercept'

        -----------------------------------------------------------------------
        """
    )

    #  read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    arg_lib.add_args(parser, 'io_in', 'io_out')

    # specify columns to histogram
    parser.add_argument("-m", "--model", type=str, nargs=1, required=True,
                        help="The model expressed in patsy syntax")

    msg = "Return input with fit and residual appended"
    parser.add_argument("--fit", action="store_true", dest='retfit',
                        default=False, help=msg)

    parser.add_argument("--plot", action="store_true",
                        default=False, help="Make residual plots")

    # parse arguments
    args = parser.parse_args()

    # get the input dataframe
    df = io_lib.df_from_input(args)

    # fit the model and add fit, resid columns
    result = sm.ols(formula=args.model[0], data=df).fit()
    df['fit_'] = result.fittedvalues
    df['resid_'] = result.resid

    # add and output the fit results if requested
    if args.retfit:
        io_lib.df_to_output(args, df)
        return

    # print the fit summary
    sys.stdout.write('\n{}\n'.format(result.summary()))
    sys.stdout.flush()

    # do plots if requested
    if args.plot:
        module_checker_lib.check_for_modules(['matplotlib', 'seaborn'])
        plot_lib = get_module('pandashells.lib.plot_lib')
        mpl = get_module('matplotlib')
        pl = get_module('pylab')
        sns = get_module('seaborn')

        pl.subplot(211)
        pl.plot(df.fit_, df.resid_, '.', alpha=.5)
        pl.xlabel('Fit')
        pl.ylabel('Residual')
        pl.title(args.model[0])

        pl.subplot(212)
        sns.distplot(df.resid_, bins=50)
        pl.xlabel('Residual with R^2 = {:0.4f}'.format(result.rsquared))
        pl.ylabel('Counts')

        # annoying issue with osx backend forces if statement here
        if mpl.get_backend().lower() in ['agg', 'macosx']:
            pl.gcf().set_tight_layout(True)
        else:
            pl.gcf().tight_layout()

        plot_lib.show(args)


if __name__ == '__main__':  # pragma: no cover
    main()
