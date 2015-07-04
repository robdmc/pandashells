#!/usr/bin/env python

import os
from setuptools import setup, find_packages
import glob

fileDir = os.path.dirname(__file__)

setup(
    name="pandashells",
    version="0.2.0",
    author="Rob deCarvalho",
    author_email="unlisted",
    description=("Command line data tools"),
    license="BSD",
    keywords="pandas plot plotting data dataframe command line cli statistics stats",
    url="https://github.com/robdmc/pandashells",
    packages=find_packages(),
    package_data={'pandashells': ['example_data/*.csv']},
    # include_package_data=True,
    long_description='Bringing the power of pandas to the command line',
    classifiers=[
        "Topic :: Utilities",
        "License ::  Simplified BSD License",
    ],
    entry_points={
        'console_scripts': [
            'p.cdf = pandashells.bin.p_cdf:main',
            'p.config = pandashells.bin.p_config:main',
            'p.crypt = pandashells.bin.p_crypt:main',
            'p.df = pandashells.bin.p_df:main',
            'p.hist = pandashells.bin.p_hist:main',
            'p.linspace = pandashells.bin.p_linspace:main',
            'p.merge = pandashells.bin.p_merge:main',
            'p.parallel = pandashells.bin.p_parallel:main',
            'p.plot = pandashells.bin.p_plot:main',
            'p.rand = pandashells.bin.p_rand:main',
            'p.regress = pandashells.bin.p_regress:main',
            'p.sig_edit = pandashells.bin.p_sig_edit:main',
        ],
    }
)
