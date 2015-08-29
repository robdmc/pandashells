#!/usr/bin/env python

import os
from setuptools import setup, find_packages

fileDir = os.path.dirname(__file__)

LONG_DESCRIPTION = """
Pandashells is a set of unix command-line tools that provide accessibility
to the python data stack directly from the bash prompt.  Users can utilize
pandas-based data-munging, perform linear regression, and even take
the spectral decomposition of non-uniformly sampled time series.
"""

setup(
    name="pandashells",
    version="0.1.5",
    author="Rob deCarvalho",
    author_email="unlisted",
    description=("Command line data tools"),
    license="BSD",
    keywords="pandas plot plotting data dataframe command line cli statistics stats",
    url="https://github.com/robdmc/pandashells",
    packages=find_packages(),
    package_data={'pandashells': ['example_data/*.csv']},
    # include_package_data=True,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
    ],
    # If you add/remove a requirement, please also update full
    extras_require={
        'console': [
            'numpy', 'pandas', 'scipy', 'patsy', 'statsmodels', 'scikit-learn',
            'supersmoother', 'gatspy',
        ],
        'full': [
            'numpy', 'pandas', 'scipy', 'patsy', 'statsmodels', 'scikit-learn',
            'supersmoother', 'gatspy', 'matplotlib', 'jinja2', 'mpld3',
            'seaborn',
        ],
    },
    entry_points={
        'console_scripts': [
            'p.config = pandashells.bin.p_config:main',
            'p.crypt = pandashells.bin.p_crypt:main',
            'p.format = pandashells.bin.p_format:main',
            'p.parallel = pandashells.bin.p_parallel:main',

            'p.df = pandashells.bin.p_df:main',
            'p.example_data = pandashells.bin.p_example_data:main',
            'p.linspace = pandashells.bin.p_linspace:main',
            'p.merge = pandashells.bin.p_merge:main',
            'p.rand = pandashells.bin.p_rand:main',
            'p.regress = pandashells.bin.p_regress:main',
            'p.sig_edit = pandashells.bin.p_sig_edit:main',
            'p.smooth = pandashells.bin.p_smooth:main',

            'p.cdf = pandashells.bin.p_cdf:main',
            'p.facet_grid = pandashells.bin.p_facet_grid:main',
            'p.hist = pandashells.bin.p_hist:main',
            'p.plot = pandashells.bin.p_plot:main',
            'p.regplot = pandashells.bin.p_regplot:main',

            'p.lomb_scargle = pandashells.bin.p_lomb_scargle:main',
        ],
    }
)
