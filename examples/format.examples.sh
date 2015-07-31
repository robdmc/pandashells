#! /usr/bin/env bash

# p.format
seq 10 | p.df --names n -i noheader | p.format -t 'touch gctmp/file{n:02d}.txt' > /dev/null

