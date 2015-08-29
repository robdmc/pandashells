# This makefile runs the steps needed to build for all supported platforms
# and upload to binstar
SHELL := /bin/bash

base: 
	conda build --python 2.7 --python 3.3 --python 3.4 .
	touch base

linux-32 :  base
	conda build --python 2.7 --python 3.3 --python 3.4 --output . \
	| p.format -t 'conda convert --platform linux-32 {c0}' -i noheader | bash -

linux-64 :  base
	conda build --python 2.7 --python 3.3 --python 3.4 --output . \
	| p.format -t 'conda convert --platform linux-64 {c0}' -i noheader | bash -

osx-64 :  base
	conda build --python 2.7 --python 3.3 --python 3.4 --output . \
	| p.format -t 'conda convert --platform osx-64 {c0}' -i noheader | bash -

all : linux-32 linux-64 osx-64

upload : all
	binstar upload */*.bz2

remove :
	binstar remove robdmc/pandashells

clean :
	rm base
	rm -rf linux-32 2>/dev/null
	rm -rf linux-64 2>/dev/null
	rm -rf osx-64 2>/dev/null

