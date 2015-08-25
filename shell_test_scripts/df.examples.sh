#! /usr/bin/env bash

# p.df
p.example_data -d tips | p.df -o table | head > /dev/null
p.example_data -d tips | head | p.df -o json > /dev/null
p.example_data -d tips | head | p.df -o json | p.df -i json -o table > /dev/null


p.example_data -d tips | p.df 'df[df.sex=="Female"]' 'df[df.smoker=="Yes"]' -o table > /dev/null
p.example_data -d tips | p.df 'df[["total_bill", "tip"]].head()' -o table > /dev/null
p.example_data -d tips | p.df 'df.groupby(by=["sex", "smoker"]).tip.sum()' -o table index > /dev/null
p.example_data -d tips | p.df 'df.groupby(by="day").total_bill.sum().plot(kind="barh")' --xlabel 'Dollars' --title 'Total Bills by Day' &
seq 10 | awk '{print $1, 2*$1}' | p.df --names a b -i table noheader | p.df -o table noheader > /dev/null

