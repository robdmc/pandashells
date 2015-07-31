#! /usr/bin/env bash

# p.rand
p.rand -n 1000 -t uniform --min=0 --max=1 | p.hist --names uniform &
p.rand -n 1000 -t normal --mu=0 --sigma=1 | p.hist --names normal &
p.rand -n 1000 -t poisson --mu=1 | p.hist --names poisson &
p.rand -n 1000 -t beta --alpha=2 --beta=6 | p.hist --names beta &
p.rand -n 1000 -t gamma --alpha=1 --beta=1 | p.hist --names gamma &
p.rand -n 1000 -t binomial --N=10 --p=0.4 | p.hist --names binomial &

