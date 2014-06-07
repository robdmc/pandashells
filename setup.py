#!/usr/bin/env python

import os
import sys
from setuptools import setup, find_packages
import glob

fileDir = os.path.dirname(__file__)

scripts = glob.glob(os.path.join(fileDir,'pandashells', 'bin', 'p.*'))

setup(
    name = "pandashells",
    version = "0.0.1",
    author = "Rob deCarvalho",
    author_email = "unlisted",
    description = ("Pipeline data tools"),
    license = "BSD",
    keywords = "pandas plot plotting data dataframe command line",
    url = "https://github.com/robdmc/pandashells",
    packages = find_packages(),
    long_description='Bringing the power of pandas to the command line',
    scripts = scripts,
    classifiers=[
        "Topic :: Utilities",
        "License ::  Simplified BSD License",
    ],
)
