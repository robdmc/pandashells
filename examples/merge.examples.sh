#! /usr/bin/env bash

# p.merge
p.merge <(p.example_data -d election) <(p.example_data -d electoral_college) --how left --on state | p.df -o table | head > /dev/null

