#! /usr/bin/env python


from mock import patch
from unittest import TestCase
import pandas as pd

from pandashells.bin.p_format import (
    main,
)


class MainTests(TestCase):
    @patch(
        'pandashells.bin.p_format.sys.argv',
        'p.format -t "a={},b={}"'.split())
    @patch('pandashells.bin.p_format.io_lib.df_from_input')
    @patch('pandashells.bin.p_format.OutStream.write')
    def test_from_input_to_output(self, write_mock, input_mock):
        df_in = pd.DataFrame([
            {'a': 1, 'b': 10},
            {'a': 2, 'b': 20},
            {'a': 3, 'b': 30},
            {'a': 4, 'b': 40},
        ])
        input_mock.return_value = df_in
        main()
        self.assertEqual(len(write_mock.call_args_list), 4)
