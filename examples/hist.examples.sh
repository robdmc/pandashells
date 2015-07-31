#! /usr/bin/env bash

# p.hist
p.rand -t beta --alpha 3 --beta 10 -n 10000 | p.hist --names beta -n 50 &
paste <(p.rand -t normal -n 10000 | p.df --names normal) <(p.rand -t gamma -n 10000 | p.df --names gamma) | p.hist -i table -c normal gamma &

