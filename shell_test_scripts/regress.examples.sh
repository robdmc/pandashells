#! /usr/bin/env bash

p.example_data -d sealevel | p.regress -m 'sealevel_mm ~ year' > /dev/null
p.example_data -d sealevel  | p.df 'df["sin"] =  np.sin(2 * np.pi * df.year)'  | p.df 'df["cos"] = np.cos(2 * np.pi * df.year)'  | p.regress -m 'sealevel_mm ~ year + cos + sin' > /dev/null
p.example_data -d sealevel  | p.df 'df["sin"] =  np.sin(2 * np.pi * df.year)'  | p.df 'df["cos"] = np.cos(2 * np.pi * df.year)'  | p.regress -m 'sealevel_mm ~ year + cos + sin' --fit  | p.cdf -c 'resid_' --title 'ECDF of trend + annual' &
p.example_data -d sealevel  | p.regress -m 'sealevel_mm ~ year' --fit  | p.plot -x year -y resid_ --ylabel 'Trend removed (mm)'  --title 'Global Sea Surface Height' &
p.example_data -d sealevel | p.df 'df["year"] = df.year - df.year.iloc[0]' 'df["sealevel_mm"] = df.sealevel_mm - df.sealevel_mm.iloc[0]' | p.regress -m 'sealevel_mm ~ year - 1' --fit | p.plot -x year -y sealevel_mm fit_ --style '.' '-' --alpha .2 1 --legend best --title 'Force Zero Intercept' &
