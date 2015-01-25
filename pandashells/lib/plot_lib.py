#! /usr/bin/env python

import os
import sys
import argparse
import re

from pandashells.lib import module_checker_lib

module_checker_lib.check_for_modules(['matplotlib', 'mpld3', 'seaborn'])

import matplotlib as mpl
import pylab as pl
import seaborn as sns
import mpld3


def show(args):
    # if figure saving requested
    if hasattr(args, 'savefig') and args.savefig:
        # save html if requested
        rex_html = re.compile('.*?\.html$')
        if rex_html.match(args.savefig[0]):
            fig = pl.gcf()
            html = mpld3.fig_to_html(fig)
            with open(args.savefig[0], 'w') as outfile:
                outfile.write(html)
            return
        # save image types
        pl.savefig(args.savefig[0])
    # otherwise show to screen
    else:
        pl.show()


def set_plot_styling(args):
    # set up seaborn context
    sns.set(context=args.plot_context[0],
            style=args.plot_theme[0],
            palette=args.plot_palette[0])

    # modify seaborn slightly to look good in interactive backends
    if 'white' not in args.plot_theme[0]:
        mpl.rcParams['figure.facecolor'] = 'white'
        mpl.rcParams['figure.edgecolor'] = 'white'


def set_limits(args):
    if args.xlim:
        pl.gca().set_xlim(args.xlim)
    if args.ylim:
        pl.gca().set_ylim(args.ylim)


def set_labels_title(args):
    if args.title:
        pl.title(args.title[0])
    if args.xlabel:
        pl.xlabel(args.xlabel[0])
    if args.ylabel:
        pl.ylabel(args.ylabel[0])


def set_legend(args):
    if args.legend:
        loc = args.legend[0]
        rex = re.compile(r'\d')
        m = rex.match(loc)
        if m:
            loc = int(loc)
        else:
            loc = 'best'
        pl.legend(loc=loc)


def set_grid(args):
    if args.no_grid:
        pl.grid(False)
    else:
        pl.grid(True)


def ensure_xy_args(args):
    x_is_none = args.x is None
    y_is_none = args.y is None
    if (x_is_none ^ y_is_none):
        msg = "\nIf either x or y is specified, both must be specified\n\n"
        sys.stderr.write(msg)
        sys.exit(1)


def ensure_xy_omission_state(args, df):
    if (len(df.columns) != 2) and (args.x is None):
        msg = "\n\n x and y can be ommited only "
        msg += "for 2-column data-frames\n"
        sys.stderr.write(msg)
        sys.exit(1)


def autofill_plot_fields_and_labels(args, df):
    # add labels for two column inputs
    if (args.x is None) and (len(df.columns) == 2):
        args.x = [df.columns[0]]
        args.y = [df.columns[1]]
    # if no xlabel, set it to the x field
    if args.xlabel is None:
        args.xlabel = args.x
    # if no ylabel, and only 1 trace being plotted, set ylabel to that field
    if (args.ylabel is None) and (len(args.y) == 1):
        args.ylabel = [args.y[0]]


def draw_traces(args, df):
    y_field_list = args.y
    x = df[args.x]
    for y_field in y_field_list:
        y = df[y_field]
        pl.plot(x, y, args.style[0], label=y_field, alpha=args.alpha[0])

def refine_plot(args):
    set_limits(args)
    set_labels_title(args)
    set_grid(args)
    set_legend(args)

def draw_xy_plot(args, df):
    ensure_xy_args(args)
    ensure_xy_omission_state(args, df)
    autofill_plot_fields_and_labels(args, df)
    draw_traces(args, df)
    refine_plot(args)
    show(args)
