#! /usr/bin/env bash

# p.parallel
time seq 10 | p.format -t 'sleep 1; echo done {n}' --names n -i noheader | p.parallel -n 1 > /dev/null
time seq 10 | p.format -t 'sleep 1; echo done {n}' --names n -i noheader | p.parallel -n 10 > /dev/null
time seq 10 | p.format -t 'sleep 1; echo done {n}' --names n -i noheader | p.parallel -n 10 -c -s stdout > /dev/null
seq 100 | p.format -t 'sleep 1; echo done {n}' --names n -i noheader | p.parallel -n 50 -v | grep __job__ | p.df 'df.dropna()' 'df.duration_sec.hist(bins=20)' &

