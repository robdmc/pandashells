#! /usr/bin/env python
import argparse
import copy
import json
import os
import sys
import StringIO
import subprocess
import tempfile


from mock import patch, MagicMock, call
from unittest import TestCase
import pandas as pd

from pandashells.lib import arg_lib, config_lib
import pandashells.bin.p_df
#from pandashells.bin.p_sig_edit import (
#    xxx,
#)




class TestNothing(TestCase):
    def test_nothing(self):
        print
        print 'doin it'

