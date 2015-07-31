#! /usr/bin/env bash

# p.regplot
p.linspace 0 10 20  | p.df 'df["y_true"] = .2 * df.x'  'df["noise"] = np.random.randn(20)'  'df["y"] = df.y_true + df.noise' --names x  | p.regplot -x x -y y &
p.linspace 0 10 40  | p.df 'df["y_true"] = .5 * df.x + .3 * df.x ** 2' 'df["noise"] = np.random.randn(40)'  'df["y"] = df.y_true + df.noise' --names x  | p.regplot -x x -y y --order 2 &
p.example_data -d sealevel | p.regplot -x year -y sealevel_mm --n_boot 1  &
