#! /usr/bin/env bash

p.rand -n 1000 -t gamma --alpha=3 --beta=.01 | p.df 'df["c1"] = df.c0' | p.sig_edit -c c1 -t 2.5 | p.df 'pd.melt(df)' --names raw edited | p.facet_grid --hue variable --map pl.hist --args value --kwargs 'alpha=.2' 'range=[0, 1000]' 'bins=50' &

