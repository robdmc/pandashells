#! /usr/bin/env bash

# p.cdf 
p.rand -t normal -n 10000 | p.cdf -c c0 > /dev/null
p.rand -t normal -n 10000 | p.cdf -c c0 -q | head > /dev/null

# p.config 
p.config > /dev/null
p.config --force_defaults > /dev/null
p.config --io_input_header noheader --io_input_type table > /dev/null
p.config --io_output_header noheader --io_output_type table > /dev/null

#p.crypt
echo 'plain text' > file.txt && p.crypt -i file.txt -v -o file.txt.crypt && p.crypt -d -i file.txt.crypt -o file_restored.txt

# p.df
p.example_data -d tips | p.df -o table | head > /dev/null
p.example_data -d tips | p.df 'df[df.sex=="Female"]' 'df[df.smoker=="Yes"]' -o table > /dev/null
p.example_data -d tips | p.df 'df[["total_bill", "tip"]].head()' -o table > /dev/null
p.example_data -d tips | p.df 'df.groupby(by=["sex", "smoker"]).tip.sum()' -o table index > /dev/null
p.example_data -d tips | p.df 'df.groupby(by="day").total_bill.sum().plot(kind="barh")' --xlabel 'Dollars' --title 'Total Bills by Day' &
seq 10 | awk '{print $1, 2*$1}' | p.df --names a b -i table noheader | p.df -o table noheader > /dev/null

# p.example_data
p.example_data -d tips | head > /dev/null
p.example_data -d sealevel | head > /dev/null
p.example_data -d election | head > /dev/null
p.example_data -d electoral_college | head > /dev/null

# p.facet_grid
p.example_data -d tips | p.facet_grid --row smoker --col sex --hue day --map pl.scatter --args total_bill tip --kwargs 'alpha=.2' 's=100' &
p.example_data -d tips | p.facet_grid --col day --row sex --hue smoker --sharex --sharey --aspect 1 --map pl.hist --args tip --kwargs 'alpha=.2' 'range=[0, 10]' 'bins=20'&

# p.format
seq 10 | p.df --names n -i noheader | p.format -t 'touch gctmp/file{n:02d}.txt' > /dev/null

# p.hist
p.rand -t beta --alpha 3 --beta 10 -n 10000 | p.hist --names beta -n 50 &
paste <(p.rand -t normal -n 10000 | p.df --names normal) <(p.rand -t gamma -n 10000 | p.df --names gamma) | p.hist -i table -c normal gamma &

# p.linspace
p.linspace 1 10 7 > /dev/null

# p.lomb_scargle
p.linspace 0 10 100 --names time | p.lomb_scargle -t time -y value --interp_exp 3 | p.plot -x period -y amp --xlim 0 3 &
p.example_data -d sealevel 'df["day"] = df.day - df.day.iloc[0]' | p.lomb_scargle -t day -y sealevel_mm --interp_exp 3 | p.df 'df[df.period < 720]' | p.plot -x period -y amp --xlim 1 400 --title 'Sea-surface height spectrum' --xlabel 'period (days)' &

# p.merge
p.merge <(p.example_data -d election) <(p.example_data -d electoral_college) --how left --on state | p.df -o table | head > /dev/null

# p.parallel
time seq 10 | p.format -t 'sleep 1; echo done {n}' --names n -i noheader | p.parallel -n 1 > /dev/null
time seq 10 | p.format -t 'sleep 1; echo done {n}' --names n -i noheader | p.parallel -n 10 > /dev/null
time seq 10 | p.format -t 'sleep 1; echo done {n}' --names n -i noheader | p.parallel -n 10 -c -s stdout > /dev/null
time seq 100 | p.format -t 'sleep 1; echo done {n}' --names n -i noheader | p.parallel -n 50 -v | grep __job__ | p.df 'df.dropna()' 'df.duration_sec.hist(bins=20)' > /dev/null

# p.plot
p.linspace 1 10 7 | p.plot -x c0 -y c0 &
p.linspace 0 6.28 100 | p.df 'df["cos"]=np.cos(df.t)' 'df["sin"]=np.sin(df.t)' --names t | p.plot -x t -y sin cos --style '.-' 'o-' --alpha 1 .2 --legend best &
p.example_data -d sealevel | p.plot -x year -y sealevel_mm --style '.' --xlabel year --ylabel 'relative sea level (mm)' --title 'Sea Level Rise' --legend best --xlim 1995 2015 &

# p.rand
p.rand -n 1000 -t uniform --min=0 --max=1 | p.hist &
p.rand -n 1000 -t normal --mu=0 --sigma=1 | p.hist &
p.rand -n 1000 -t poisson --mu=1 | p.hist &
p.rand -n 1000 -t beta --alpha=2 --beta=6 | p.hist &
p.rand -n 1000 -t gamma --alpha=1 --beta=1 | p.hist &
p.rand -n 1000 -t binomial --N=10 --p=0.4 | p.hist &

# p.regplot
p.linspace 0 10 20 'df["noise"] = np.random.randn(20)' 'df["y"] = df.y_true + df.noise' --names x | p.regplot -x x -y y &
p.linspace 0 10 40 'df["noise"] = np.random.randn(40)' 'df["y"] = df.y_true + df.noise' --names x | p.regplot -x x -y y --order 2 &
p.example_data -d sealevel | p.regplot -x year -y sealevel_mm --n_boot 1 &

# p.regress
p.example_data -d sealevel | p.regress -m 'sealevel_mm ~ year' > /dev/null
p.example_data -d sealevel | p.regress -m 'sealevel_mm ~ year + cos + sin' > /dev/null
p.example_data -d sealevel | p.regress -m 'sealevel_mm ~ year + cos + sin' --fit | p.cdf -c 'resid_' --title 'ECDF of trend + annual' &
p.example_data -d sealevel | p.regress -m 'sealevel_mm ~ year' --fit | p.plot -x year -y resid_ --ylabel 'Trend removed (mm)' --title 'Global Sea Surface Height' &
p.example_data -d sealevel | p.df 'df["year"] = df.year - df.year.iloc[0]' 'df["sealevel_mm"] = df.sealevel_mm - df.sealevel_mm.iloc[0]' | p.regress -m 'sealevel_mm ~ year - 1' --fit | p.plot -x year -y sealevel_mm fit_ --style '.' '-' --alpha .2 1 --legend best --title 'Force Zero Intercept' &

#p.sig_edit
p.rand -n 1000 -t gamma --alpha=3 --beta=.01 | p.df 'df["c1"] = df.c0' | p.sig_edit -c c1 -t 2.5 | p.df 'pd.melt(df)' --names raw edited | p.facet_grid --hue variable --map pl.hist --args value --kwargs 'alpha=.2' 'range=[0, 1000]' 'bins=50' &
