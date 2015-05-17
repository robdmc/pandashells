#! /usr/bin/env python

# standard library imports
import sys
import argparse

from pandashells.lib import module_checker_lib, arg_lib, io_lib, plot_lib

# import required dependencies
module_checker_lib.check_for_modules([
    'pandas',
    'matplotlib',
    'statsmodels',
    'seaborn',
    'numpy',
    'scipy'])

import matplotlib as mpl
import pylab as pl
import seaborn as sns
import statsmodels.formula.api as sm


def main():
    msg = "Performs (multivariable) linear regression.  Fitting model "
    msg += "is specified using the patsy language.  Input is from stdin "
    msg += "and output is either fitting information or the input data "
    msg += "with a column containing fit results and residuals appended."

    # read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    arg_lib.add_args(parser, 'io_in', 'io_out', 'example')

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
    df['_fit'] = result.fittedvalues
    df['_resid'] = result.resid

    # add and output the fit results if requested
    if args.retfit:
        io_lib.df_to_output(args, df)
        return

    # print the fit summary
    sys.stdout.write('\n{}\n'.format(result.summary()))
    sys.stdout.flush()

    # do plots if requested
    if args.plot:
        pl.subplot(211)
        pl.plot(df._fit, df._resid, '.', alpha=.5)
        pl.xlabel('Fit')
        pl.ylabel('Residual')
        pl.title(args.model[0])

        pl.subplot(212)
        sns.distplot(df._resid, bins=50)
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
