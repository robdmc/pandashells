#!/usr/bin/env python

import os
from setuptools import setup, find_packages
import glob

fileDir = os.path.dirname(__file__)

scripts = glob.glob(os.path.join(fileDir, 'pandashells', 'bin', 'p.*'))

setup(
    name="pandashells",
    version="0.0.1",
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
    # scripts=scripts,
    classifiers=[
        "Topic :: Utilities",
        "License ::  Simplified BSD License",
    ],
    entry_points={
        'console_scripts': [
            'p.config = pandashells.bin.p_config:main',
            'p.crypt = pandashells.bin.p_crypt:main',
            'p.df = pandashells.bin.p_df:main',
            'p.sig_edit = pandashells.bin.p_sig_edit:main',
            'p.merge = pandashells.bin.p_merge:main'
        ],
    }
)
