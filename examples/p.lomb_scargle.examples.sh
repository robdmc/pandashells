#! /usr/bin/env bash

# p.lomb_scargle
p.linspace 0 10 100 --names time | p.lomb_scargle -t time -y value --interp_exp 3 | p.plot -x period -y amp --xlim 0 3 &
p.example_data -d sealevel 'df["day"] = df.day - df.day.iloc[0]' | p.lomb_scargle -t day -y sealevel_mm --interp_exp 3 | p.df 'df[df.period < 720]' | p.plot -x period -y amp --xlim 1 400 --title 'Sea-surface height spectrum' --xlabel 'period (days)' &

