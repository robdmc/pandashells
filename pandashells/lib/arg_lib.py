import os
import sys
import inspect


############# dev only.  Comment out for production ######################
sys.path.append('../..')
##########################################################################

from pandashells.lib import config_lib

#=============================================================================
def addArgs(parser, *args, **kwargs):
    """
    kwargs: 'io.no_col_spec_allowed'
    """

    config_dict = config_lib.get_config()
    allowedArgSet = set(
            [
                'io_in',
                'io_out',
                'example',
                'xy_plotting',
                'decorating',
            ])

    inArgSet = set(args)
    unrecognizedSet = inArgSet - allowedArgSet
    if unrecognizedSet:
        raise Exception('Unrecognized set in addArgs')

    #-------------------------------------------------------------------------
    if 'io_in' in inArgSet:
        #--- define the valid components
        io_opt_list = ['csv', 'table','header','noheader', 'index','noindex']

        #--- allow the option of supplying input column names
        if not kwargs.get( 'io_no_col_spec_allowed', False):
            msg = 'Overwrite column names with this comma-delimited list'
            parser.add_argument('--columns', nargs=1, type=str,
                    dest='columns', metavar="'col1Name,col2Name,...'",
                    help=msg)

        #--- define the current defaults
        default_for_input = "'{},{}'".format(config_dict['io_input_type'],
                config_dict['io_input_header'])

        #--- show the current defaults in the arg parser
        msg = 'Comma delimited options taken from {}'.format(
                repr(io_opt_list))

        parser.add_argument('-i', '--input_options', nargs=1,
                 type=str, dest='input_options', metavar=default_for_input,
                 default=[default_for_input], help=msg)

    #-------------------------------------------------------------------------
    if 'io_out' in inArgSet:
        #--- define the valid components
        io_opt_list = ['csv', 'table','html',
                'header','noheader', 'index', 'noindex']

        #--- define the current defaults
        default_for_output = "'{},{},{}'".format(
              config_dict['io_output_type'],
              config_dict['io_output_header'],config_dict['io_output_index'])

        #--- show the current defaults in the arg parser
        msg = 'Comma delimited options taken from {}'.format(repr(io_opt_list))
        parser.add_argument('-o', '--output_options', nargs=1,
                 type=str, dest='output_options', metavar=default_for_output,
                 default=[default_for_output], help=msg)

    #-------------------------------------------------------------------------
    if 'decorating' in inArgSet:
        #--- 
        plot_theme_list = ['mpl', 'gray', 'grey']
        plot_page_list = ['landscape', 'portrait', 'slideFull', 'slideBumper']
        #--- 
        default_for_plotting = "{},{}".format(
              config_dict['plot_theme'], config_dict['plot_page'])
        #--- 
        msg = "Set the x-limits for the plot"
        parser.add_argument('--xlim', nargs=2, type=float, dest='xlim',
                 metavar=('XMIN', 'XMAX'), help=msg)
        #--- 
        msg = "Set the y-limits for the plot"
        parser.add_argument('--ylim', nargs=2, type=float, dest='ylim',
                 metavar=('YMIN','YMAX'), help=msg)
        #--- 
        msg = "Set the x-label for the plot"
        parser.add_argument('--xlabel', nargs=1, type=str, dest='xlabel',
                 help=msg)
        #--- 
        msg = "Set the y-label for the plot"
        parser.add_argument('--ylabel', nargs=1, type=str, dest='ylabel',
                 help=msg)
        #--- 
        msg = "Set the title for the plot"
        parser.add_argument('--title', nargs=1, type=str, dest='title',
                 help=msg)
        #--- 
        msg = "Specify legend location"
        parser.add_argument('--legend', nargs=1, type=str, dest='legend',
                 choices=['1','2','3','4','best'], help=msg)
        #--- 
        msg = "Specify whether hide the grid or not"
        parser.add_argument('--nogrid',  action='store_true', dest='no_grid',
                default=False,  help=msg)
        #--- 
        msg = 'Comma delimited options taken from {}'.format(
                repr(plot_theme_list + plot_page_list))
        parser.add_argument( '--theme', nargs=1,
                 type=str, dest='theme', metavar=default_for_plotting,
                 default=[default_for_plotting], help=msg)
    #-------------------------------------------------------------------------
    if 'xy_plotting' in inArgSet:

        #--- 
        msg = 'Column to plot on x-axis'
        parser.add_argument('-x', nargs=1, type=str, dest='x', 
                help=msg)
        #--- 
        msg = 'Comma-delimited list of columns to plot on y-axis'
        parser.add_argument('-y', nargs=1, type=str, dest='y', 
                help=msg)
        #--- 
        msg = "Plot style defaults to .-"
        parser.add_argument('-s', '--style', nargs=1, type=str, dest='style',
                default=['.-'], help=msg)


    #-------------------------------------------------------------------------
    if 'example' in inArgSet:
        msg = "Show a usage example and exit"
        parser.add_argument('--example', action='store_true', dest='example',
                default=False,  help=msg)

