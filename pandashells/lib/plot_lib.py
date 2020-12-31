#! /usr/bin/env python

import os
import re
import sys
import warnings
warnings.filterwarnings("ignore")
from dateutil.parser import parse
import matplotlib as mpl
import pylab as pl
import seaborn as sns
import mpld3


def running_in_container():
    container = False
    cgroup = '/proc/self/cgroup'
    if os.path.isfile(cgroup):
        with open(cgroup) as buff:
            container = bool(
                [line for line in buff.readlines() if 'docker' in line]
            )
    return container


def show(args):
    # if figure saving requested
    if hasattr(args, 'savefig') and args.savefig:
        # save html if requested
        rex_html = re.compile(r'.*?\.html$')
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
        if mpl.rcParams.get('backend') == 'WebAgg':
            from matplotlib.backends.backend_webagg import WebAggApplication
            in_container = running_in_container()
            if in_container:
                mpl.rcParams['webagg.address'] = '0.0.0.0'

            WebAggApplication.initialize()

            if in_container:
                display_address = '127.0.0.1'
            else:
                display_address = WebAggApplication.address

            print(
                '\nServing UI on: http://{address}:{port}'.format(
                    address=display_address,
                    port=WebAggApplication.port,
                ),
                file=sys.stderr
            )
        pl.show()


def set_plot_styling(args):
    # set up seaborn context
    warnings.filterwarnings("ignore")
    sns.set(context=args.plot_context[0],
            style=args.plot_theme[0],
            palette=args.plot_palette[0])

    # modify seaborn slightly to look good in interactive backends
    if mpl.rcParams.get('backend') != 'WebAgg':
        if 'white' not in args.plot_theme[0]:
            mpl.rcParams['figure.facecolor'] = 'white'
            mpl.rcParams['figure.edgecolor'] = 'white'


def set_limits(args):
    if args.xlim:
        pl.gca().set_xlim(args.xlim)
    if args.ylim:
        pl.gca().set_ylim(args.ylim)


def set_scale(args):
    if args.xlog:
        pl.gca().set_xscale('log')
    if args.ylog:
        pl.gca().set_yscale('log')


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


def str_to_date(x):
    try:
        basestring
    except NameError:
        basestring = str
    if isinstance(x.iloc[0], basestring):
        return [parse(e) for e in x]
    else:
        return x


def draw_traces(args, df):
    y_field_list = args.y
    x = str_to_date(df[args.x[0]])
    style_list = args.style
    alpha_list = args.alpha
    if len(style_list) != len(y_field_list):
        style_list = [style_list[0] for y_field in y_field_list]
    if len(alpha_list) != len(y_field_list):
        alpha_list = [alpha_list[0] for y_field in y_field_list]

    for y_field, style, alpha in zip(y_field_list, style_list, alpha_list):
        y = df[y_field]
        pl.plot(x, y, style, label=y_field, alpha=alpha)


def refine_plot(args):
    set_limits(args)
    set_scale(args)
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
