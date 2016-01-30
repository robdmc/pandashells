## 0.1.4 (8/1/2015)

Initial public release:


## 0.1.5 (8/29/2015)

Improved installation procedures:
```bash
  - pip install           # no dependencies
  - pip install[console]  # dependencies for console tools
  - pip install[full]     # install all dependencies
```
Added smoothing tool
  - p.smooth 

Bug fixes
  - Fixed tsv bug


## 0.1.6 (1/25/2016)

The Pandas and matplotlib api's are evolving.  Pandashells
was throwing a bunch of deprication warnings and not all tests
were passing with the latest versions of these libraries.  This
is basically a maintenance release to accomadate these changes.
Below are the highlights.

* Current versions are: pandas==0.17.1, matplotlib 1.5.1
* Fixed a bug in writing html tables
* Improved the Timer() profiling tool and added it to the docs.
