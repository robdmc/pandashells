#! /usr/bin/env bash
# build against python2 and python3
#conda build --python 2.7 --python 3.3 --python 3.4 .

# create builds for all supported architectures
conda build --python 2.7 --python 3.3 --python 3.4 --output . | p.format -t 'conda convert --platform osx-64 {c0}' -i noheader | bash -
conda build --python 2.7 --python 3.3 --python 3.4 --output . | p.format -t 'conda convert --platform linux-32 {c0}' -i noheader | bash -
conda build --python 2.7 --python 3.3 --python 3.4 --output . | p.format -t 'conda convert --platform linux-64 {c0}' -i noheader | bash -
