# This makefile runs the steps needed to build for all supported platforms
# and upload to binstar
SHELL := /bin/bash

PYTHONS := --python 2.7 --python 3.3 --python 3.4 --python 3.5

base: 
	pip install -U pip
	#pip install -U pandashells
	conda install anaconda-client
	conda build ${PYTHONS} .
	touch base

linux-32 :  base
	conda build ${PYTHONS} --output . \
	| awk '{print "conda convert --platform linux-32", $$1 }' | bash -

linux-64 :  base
	conda build --python 2.7 --python 3.3 --python 3.4 --python 3.5 --output . \
	| awk '{print "conda convert --platform linux-64", $$1 }' | bash -

osx-64 :  base
	conda build --python 2.7 --python 3.3 --python 3.4 --python 3.5 --output . \
	| awk '{print "conda convert --platform osx-64", $$1 }' | bash -

all : linux-32 linux-64 osx-64

upload : all
	anaconda upload */*.bz2

remove :
	anaconda remove robdmc/pandashells

clean :
	rm base 2>/dev/null || true
	rm -rf linux-32 2>/dev/null || true
	rm -rf linux-64 2>/dev/null || true
	rm -rf osx-64 2>/dev/null || true

