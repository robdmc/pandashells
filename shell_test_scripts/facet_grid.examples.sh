#! /usr/bin/env bash

# p.facet_grid
p.example_data -d tips | p.facet_grid --row smoker --col sex --hue day --map pl.scatter --args total_bill tip --kwargs 'alpha=.2' 's=100' &
p.example_data -d tips | p.facet_grid --col day --row sex --hue smoker --sharex --sharey --aspect 1 --map pl.hist --args tip --kwargs 'alpha=.2' 'range=[0, 10]' 'bins=20'&
