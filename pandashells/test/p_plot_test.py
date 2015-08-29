#! /usr/bin/env python
from mock import patch, MagicMock
from unittest import TestCase

from pandashells.bin.p_plot import main


class MainTests(TestCase):
    @patch('pandashells.bin.p_plot.argparse.ArgumentParser')
    @patch('pandashells.bin.p_plot.arg_lib.add_args')
    @patch('pandashells.bin.p_plot.io_lib.df_from_input')
    @patch('pandashells.bin.p_plot.plot_lib.set_plot_styling')
    @patch('pandashells.bin.p_plot.plot_lib.draw_xy_plot')
    def test_plotting(
            self, draw_xy_mock, set_plot_styling_mock, df_from_input_mock,
            add_args_mock, ArgumentParserMock):
        args = MagicMock()
        parser = MagicMock(parse_args=MagicMock(return_value=args))
        ArgumentParserMock.return_value = parser
        df_from_input_mock.return_value = 'df'

        main()

        add_args_mock.assert_called_with(
            parser, 'io_in', 'xy_plotting', 'decorating')

        df_from_input_mock.assert_called_with(args)
        set_plot_styling_mock.assert_called_with(args)
        draw_xy_mock.assert_called_with(args, 'df')
