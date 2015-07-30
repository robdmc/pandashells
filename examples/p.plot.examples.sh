#! /usr/bin/env bash

# p.plot
p.linspace 1 10 7 | p.plot -x c0 -y c0 &
p.linspace 0 6.28 100 | p.df 'df["cos"]=np.cos(df.t)' 'df["sin"]=np.sin(df.t)' --names t | p.plot -x t -y sin cos --style '.-' 'o-' --alpha 1 .2 --legend best &
p.example_data -d sealevel | p.plot -x year -y sealevel_mm --style '.' --xlabel year --ylabel 'relative sea level (mm)' --title 'Sea Level Rise' --legend best --xlim 1995 2015 &

