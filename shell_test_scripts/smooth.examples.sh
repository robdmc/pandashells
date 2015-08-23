#! /usr/bin/env bash

# smooth
p.example_data -d sealevel | p.df 'df["smoothed"] = df.sealevel_mm' | p.smooth -y smoothed | p.plot -x year -y sealevel_mm smoothed --legend best -s . '-' --alpha .5 1 &
