# This is just an example of how one can use make files in a data science 
# chain.  It is still an undocumented work in progress, but feel free to
# play with it.

SHELL := /bin/bash
D := ./out/

clean:
	rm -rf $(D)

$(D)raw_data.csv:
	mkdir -p $(D)
	p.example_data -d sealevel > $@

$(D)raw_plot.html: $(D)raw_data.csv
	cat $< | p.plot -x year -y sealevel_mm --savefig $@
	
$(D)reg_plot.html: $(D)raw_data.csv
	cat $< | p.regplot -x year -y sealevel_mm --n_boot 1 --savefig $@

$(D)trend_removed.csv: $(D)raw_data.csv
	cat $< | p.regress -m 'sealevel_mm ~ year' --fit > $@

$(D)trend_removed.html: $(D)trend_removed.csv
	cat $< | p.plot -x year -y resid_ --savefig $@

$(D)spectrum.csv: $(D)trend_removed.csv
	cat $< | p.lomb_scargle -t year -y resid_ --interp_exp 3 > $@

$(D)spectrum.html: $(D)spectrum.csv
	cat $< | p.plot -x period -y amp --savefig $@

$(D)raw_with_regressors.csv: $(D)raw_data.csv
	cat $< \
	| p.df 'df["s1"] =  np.sin(2 * np.pi * df.year)' \
	| p.df 'df["c1"] = np.cos(2 * np.pi * df.year)' \
	| p.df 'df["s2"] = np.sin(2 * np.pi * df.year / .1608)' \
	| p.df 'df["c2"] = np.cos(2 * np.pi * df.year / .1608)' \
	| p.df 'df["s3"] = np.sin(2 * np.pi * df.year / 13.328)' \
	| p.df 'df["c3"] = np.cos(2 * np.pi * df.year / 13.328)'   > $@

$(D)full_regression.csv: $(D)raw_with_regressors.csv
	cat $< | p.regress -m \
	'sealevel_mm ~ year + s1 + c1 + s2 + c2 +s3 + c3' --fit > $@

$(D)regressed_model.html: $(D)full_regression.csv
	cat $< | p.plot -x year -y sealevel_mm fit_ --savefig $@

$(D)regressed_model_resid.html: $(D)full_regression.csv
	cat $< | p.hist -c resid_ -n 30 --savefig $@

all: $(D)raw_plot.html $(D)reg_plot.html  $(D)trend_removed.html \
	 $(D)spectrum.html $(D)regressed_model.html $(D)regressed_model_resid.html

