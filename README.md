PANDASHELLS                           
===

Description
-------------------------------------------------------------------------------
The ptools library was written to bring the power of the python scienctific
stack to the unix command-line. This allows well-known and time-tested tools 
like grep, awk, sed, etc. to interact seemlessly with the powerful data
manipulation, visualization, and statistical libraries being developed in the 
python data-science community.


Installation
--------------------------------------------------------------------------------
  --- master branch
  pip install git+https://github.com/robdmc/ptools.git

  --- experimental branch with pandas (very early stage developement
  pip install git+https://github.com/robdmc/ptools.git@with_pandas


List of tools (run with -h for help, --example to see example)
--------------------------------------------------------------------------------
 p.df       Pandas dataframe manipulation of csv files


*********** here are some new tools I want
p.lombscargle
p.mcmc 'patsy model'  (see if there's an easy way to do this)
                      Maybe make distribution,params,prior for each variable
                      p.mcmc 'y ~ x + z' 'x:Normal(mu, sigma)', y:Normal(mu,sigma)
                      think about defaults here where partials don't have noise

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
here are some regression and classification ideas.

p.regress - statmodels linear regression with full summary output. maybe use --fit to add fit results to df
p.learn.regress_linear
p.learn.regress_ridge
p.learn.regress_tree
p.learn.regress_forest
p.learn.classify.logistic
p.learn.classify.tree
p.learn.classify.forest
p.learn.classify.svm

Always use patsy language

the model.pkl files (which can be user-def names) hold the model as well
as the string used to do the fit

with --fit model.pkl
saves model in model.pkl and displays rms R^2 and cross_val scores
as well as the original string used to do the fit and the type of model


with --predict model.pkl
loads model, input and shows _fit variable to the dataframe
with --stats, does same thing, but displays rms and R2
with --hist shows hist of residuals
with --plot shows fit vs residual

of course classifiers have their own metrics and maybe have a
--roc that plots the roc curve

with
--info model.pkl, just shows the model

with --desc 'my desc'  allows you to store a description that will be
                       displayed with the --info flag



++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




 ********** here is list of tools I want to replicate *********************
p.cov -> covariance between collumns.  cols and index have respective names
*p.parallel
*p.plot
*p.geoCode
*p.crypt
p.bar
p.cdf
p.color
p.fft
p.lombscargle
p.hist
p.interp # cat xvals_file | p.interp -r .6 -t <(cat table_file.txt)
p.linspace
p.map
p.mapDots2html
p.mapPoly2html
p.mongoDump
p.normalize
p.pgsql2csv
p.pie
p.rand
p.regress
p.scat
p.server
p.shuffle
p.sigEdit
p.smooth   lowess, spline, medianFilter
p.sshKeyPush
p.template
p.utc2local
