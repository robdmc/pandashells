#! /usr/bin/env python

#--- standard library imports
import os
import sys
import argparse
import re

############# dev only.  Comment out for production ######################
sys.path.append('../..')
##########################################################################


from pandashells.lib import module_checker_lib

#--- import required dependencies
modulesOkay = module_checker_lib.check_for_modules(
        [
            'matplotlib',
        ])
if not modulesOkay:
    sys.exit(1)

import matplotlib as mpl
import pylab as pl

#=============================================================================
#===== FILL IN RC PARAMS FOR EACH THEME DICT =================================
#--- initialize a dict to hold all themes
THEME_DICT = {}
PAGE_SET = set(['slideFull', 'slideBumper', 'portrait', 'landscape'])


#-----------------------------------------------------------------------------
#--- matplotlib theme
rcd = {
    'figure.figsize': '6, 4',
    "figure.figsize": "11, 8",
    'figure.facecolor': 'white',
    'figure.edgecolor': 'white',
    'font.size': '10',
    'savefig.dpi': 72,
    #'figure.subplot.bottom' : .125
        }
THEME_DICT['mpl'] = rcd

#-----------------------------------------------------------------------------
#--- define the slightly modified ggplot theme
rcd = {}
rcd["timezone"] = "UTC"
rcd["lines.linewidth"] = "1.0"
rcd["lines.antialiased"] = "True"
rcd["patch.linewidth"] = "0.5"
rcd["patch.facecolor"] = "348ABD"
rcd["patch.edgecolor"] = "#E5E5E5"
rcd["patch.antialiased"] = "True"
rcd["font.family"] = "sans-serif"
rcd["font.size"] = "14.0"
rcd["font.weight"] = "300"
rcd["font.serif"] = ["Times", "Palatino", "New Century Schoolbook",
                             "Bookman", "Computer Modern Roman",
                             "Times New Roman"]
rcd["font.sans-serif"] = ["Helvetica", "Avant Garde",
                                  "Computer Modern Sans serif", "Arial"]
rcd["axes.facecolor"] = "#E5E5E5"
rcd["axes.edgecolor"] = "bcbcbc"
rcd["axes.linewidth"] = "1"
rcd["axes.grid"] = "True"
rcd["axes.titlesize"] = "x-large"
rcd["axes.labelsize"] = "large"
rcd["axes.labelcolor"] = "black"
rcd["axes.axisbelow"] = "True"
rcd["axes.color_cycle"] = [
        "348ABD",
        "A60628",
        "467821",
        "#333333",
        "7A68A6",
        "CF4457",
        "188487",
        "E24A33"
        ]
rcd["grid.color"] = "white"
rcd["grid.linewidth"] = "1.4"
rcd["grid.linestyle"] = "solid"
rcd["xtick.major.size"] = "0"
rcd["xtick.minor.size"] = "0"
rcd["xtick.major.pad"] = "6"
rcd["xtick.minor.pad"] = "6"
rcd["xtick.color"] = "#7F7F7F"
rcd["xtick.direction"] = "out"  # pointing out of axis
rcd["ytick.major.size"] = "0"
rcd["ytick.minor.size"] = "0"
rcd["ytick.major.pad"] = "6"
rcd["ytick.minor.pad"] = "6"
rcd["ytick.color"] = "#7F7F7F"
rcd["ytick.direction"] = "out"  # pointing out of axis
rcd["legend.fancybox"] = "True"
rcd["figure.figsize"] = "11, 8"
rcd["figure.facecolor"] = "1.0"
rcd["figure.edgecolor"] = "0.50"
rcd["figure.subplot.hspace"] = "0.5"
rcd['savefig.dpi'] =  72
THEME_DICT['gray'] = rcd
THEME_DICT['grey'] = rcd

#-----------------------------------------------------------------------------
#--- define slide full
def set_slideFull(rcd):
    rcd["font.family"] = "sans-serif"
    rcd["font.size"] = "14.0"
    rcd["font.weight"] = "bold"
    rcd['axes.titlesize'] = "18"
    rcd['axes.labelsize'] = "16"
    #rcd['axes.linewidth'] = "2"
    rcd["xtick.major.size"] = "7"
    rcd["ytick.major.size"] = "7"
    rcd['xtick.major.pad'] = "6"
    rcd['ytick.major.pad'] = "6"
    rcd['lines.linewidth'] = "2"
    rcd['lines.markersize'] = "7"
    rcd["figure.figsize"] = ["8.8", "5.9"]
    rcd['savefig.dpi'] = "300"
    rcd['figure.subplot.bottom'] = .125

def set_bumper(rcd):
    set_slideFull(rcd)
    rcd["figure.figsize"] = [8.8, 4.9]
def set_portrait(rcd):
    set_slideFull(rcd)
    rcd["figure.figsize"] = [8.5, 11]
def set_landscape(rcd):
    set_slideFull(rcd)
    rcd["figure.figsize"] = [11, 8.5]


#=============================================================================
def set_theme_and_page(theme_name, page_name):
    #--- make sure theme is recognized
    if not theme_name in THEME_DICT:
        msg = "Theme '{}' not recognized. ".format(theme_name)
        msg += "Select them from {}".format(str(THEME_DICT.keys()))

    #--- get the approriate rc ddict
    rcd = THEME_DICT[theme_name]

    #--- overwrite relevant page info
    if page_name == 'slideFull':
        set_slideFull(rcd)
    elif page_name == 'slideBumper':
        set_bumper(rcd)
    elif page_name == 'portrait':
        set_portrait(rcd)
    elif page_name == 'landscape':
        set_landscape(rcd)

    #--- set the params
    for k, v in rcd.iteritems():
        sys.stdout.flush()
        if v:
            mpl.rcParams[k] = v

#=============================================================================
def set_theme(args):
    if hasattr(args, 'theme'):
        theme_name = list(set(args.theme[0].split(',')).intersection(
            set(THEME_DICT.keys())))[0]
        page_name = list(
                set(args.theme[0].split(',')).intersection( PAGE_SET))[0]
    else:
        theme_name = 'gray'
        page_name = 'slideFull'
    set_theme_and_page(theme_name, page_name)


#=============================================================================
def refine_plot(args):
    if args.xlim:
        pl.gca().set_xlim(args.xlim)
    if args.ylim:
        pl.gca().set_ylim(args.ylim)
    if args.title:
        pl.title(args.title[0])
    if args.xlabel:
        pl.xlabel(args.xlabel[0])
    if args.ylabel:
        pl.ylabel(args.ylabel[0])
    if args.legend:
        loc = args.legend[0]
        rex = re.compile(r'\d')
        m = rex.match(loc)
        if m:
            loc = int(loc)

        pl.legend(loc=loc)
    if args.no_grid:
        pl.grid(False)
    else:
        pl.grid(True)

#=============================================================================
def draw_xy_plot(args, df):
    if ((args.x is None) and (not args.y is None)) or \
            ((args.y is None) and (not args.x is None)):
        msg = "\nIf either x or y is specified, both must be specified\n\n"
        sys.stderr.write(msg)
        sys.exit(1)

    if len(df.columns) != 2:
        if args.x is None:
                msg = "\n\n x and y can be ommited only "
                msg += "for 2-column data-frames\n"
                sys.stderr.write(msg)
                sys.exit(1)
    if ( args.x is None) and (len(df.columns) == 2):
        args.x = [df.columns[0]]
        args.y = [df.columns[1]]
    if args.xlabel is None:
        args.xlabel = args.x
    if args.ylabel is None:
        args.ylabel = args.y

    y_field_list = args.y[0].split(',')
    x = df[args.x]
    for y_field in y_field_list:
        y = df[y_field]
        pl.plot(x, y, args.style[0], label=y_field)

    refine_plot(args)
    pl.show()
