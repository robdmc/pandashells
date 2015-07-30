#! /usr/bin/env bash

# p.cdf 
p.rand -t normal -n 10000 | p.cdf -c c0 > /dev/null
p.rand -t normal -n 10000 | p.cdf -c c0 -q | head > /dev/null


