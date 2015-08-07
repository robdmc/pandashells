#!/bin/bash

$PYTHON setup.py install

pip install --no-cache-dir mpld3
pip install --no-cache-dir astroML
pip install --no-cache-dir supersmoother
pip install --no-cache-dir gatspy

# Add more build steps here, if they are necessary.

# See
# http://docs.continuum.io/conda/build.html
# for a list of environment variables that are set during the build process.
