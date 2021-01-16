
Pandashells                           
===

Introduction
---
For decades, system administrators, dev-ops engineers and data analysts have been
piping textual data between unix tools like grep, awk, sed, etc.  Chaining these
tools together provides an extremely powerful workflow.

The more recent emergence of the "data-scientist" has resulted in the increasing
popularity of tools like R, Pandas, IPython, etc.  These tools have amazing power
for transforming, analyzing and visualizing data-sets in ways that grep, awk,
sed, and even the dreaded perl-one-liner could never accomplish.

Pandashells is an attempt to marry the expressive, concise workflow of the shell pipeline
with the statistical and visualization tools of the python data-stack.


What is Pandashells?
----
* A set of command-line tools for working with tabular data
* Easily read/write data in CSV, or space delimited formats
* Quickly aggregate, join, and summarize tabular data 
* Compute descriptive statistics
* Perform spectral decomposition and linear regression
* Create data visualizations that can be saved to images or rendered interactively using 
  either a native backend or html.
* Easily integrate with unix tools like curl, awk, grep, sed, etc.

If you work with data using Python, you have almost certainly encountered 
<a href="http://pandas.pydata.org/">Pandas</a>,
<a href="http://www.scipy.org/">SciPy</a>, 
<a href="http://matplotlib.org/">Matplotlib</a>, 
<a href="http://statsmodels.sourceforge.net/">Statsmodels</a> and
<a href="http://stanford.edu/~mwaskom/software/seaborn/">Seaborn</a>.  Pandashells
opens up a bash API into the python data stack with command syntax
closely mirroring the underlying libraries on which it is built.  This should
allow those familiar with the python data stack to be immediately productive.


Installation
----

### Install with pip
Pandashells can be installed with pip, but a few words of caution are in order.  First,
you should really use a recent version of pip so you can access wheels on pypi
`pip install -U pip`.  Secondly, if your setup requires building from source rather
than using wheels, you may run into problems with systems libraries being either out of
date or missing.  If you encounter these problems, you may want to use conda to install those
dependencies.

#### Pandashells, no dependencies
Use this option if you want to completely manage your own dependencies.
(See requirements section below).

<pre><code><strong> [~]$ pip install pandashells </strong></code></pre>

#### Pandashells console tools
Use this option to install Pandashells and only the console tools dependencies. This
will not install the graphics dependencies (matplotlib and friends)
<pre><code><strong>[~]$ pip install pandashells[console]</strong></code></pre>

#### Pandashells full install
Use this option to install Pandashells and all dependencies
<pre><code><strong>[~]$ pip install pandashells[full]</strong></code></pre>

Requirements
----
Pandashells is both Python2 and Python3 compatible.  There are no default requirements
because some of the tools only require the standard library, and there's no sense installing
unnecessary packages if you only want to use that subset of tools.  If a particular tool
encounters a missing dependency, it will fail with an error message indicating the missing
dependency.  Below is a list of all imports used across the Pandashells toolkit, and ordered
according to install option.
* `[console]`  numpy, scipy, pandas, statsmodels, gatspy, supersmoother
* `[full]` numpy, scipy, pandas, statsmodels, gatspy, supersmoother, matplotlib, mpld3, seaborn


**Important:**  If you want to use pandashells without interactive visualizations
(e. g. on a VM without X-forwarding), but would like to retain the ability to
create static-image or html-based visualizations, you may need to configure pandashells to
use the Agg backend as follows:
<pre><code>p.config --plot_backend Agg</code></pre>


Overview
----

All Pandashells executables begin with a "p."  This is designed to work
nicely with the bash-completion feature.  If you can't remember the exact
name of a command, simply typing p.[tab] will show you a complete list of
all Pandashells commands.

Every command can be run with a -h option to view help.  Each of these
help messages will contain multiple examples of how to properly use the tool.

Pandashells is equipped with a tool to generate sample csv files.  This tool
provides standardized inputs for use in the tool help sections as well as this
documentation.
<pre><code><strong>[~]$ p.example_data -h</strong></code></pre>
  
Tool Descriptions
---

Tool          |pip install           |Purpose
---           |---                   |---
p.config      |`pandashells`         |Set default Pandashells configuration options
p.crypt       |`pandashells`         |Encrypt/decrypt files using open-ssl
p.format      |`pandashells`         |Render python string templates using input data
p.gui         |`pandashells`         |Open dataframe in pandasgui interactive environment
p.parallel    |`pandashells`         |Read shell commands from stdin and run them in parallel
p.example_data|`pandashells`         |Create sample csv files for training/testing
p.df          |`pandashells[console]`|Pandas dataframe manipulation of text files
p.linspace    |`pandashells[console]`|Generate a linearly spaced series of numbers
p.lomb_scargle|`pandashells[console]`|Generate Lomb-Scarge spectrogram of input time series
p.merge       |`pandashells[console]`|Merge two data files by specifying join keys
p.rand        |`pandashells[console]`|Generate random numbers
p.regress     |`pandashells[console]`|Perform (multi-variate) linear regression with R-like patsy syntax
p.sig_edit    |`pandashells[console]`|Remove outliers using iterative sigma-editing
p.smooth      |`pandashells[console]`|Smooth data
p.cdf         |`pandashells[full]`   |Plot emperical distribution function
p.facet_grid  |`pandashells[full]`   |Create faceted plots for data exploration
p.hist        |`pandashells[full]`   |Plot histograms
p.plot        |`pandashells[full]`   |Create xy plot visualizations
p.regplot     |`pandashells[full]`   |Quickly plot linear regression of data to a polynomial


DataFrame Manipulations
----
Pandashells allows you to specify multiple dataframe operations in a single command.
Each operation assumes data is in a dataframe named `df`.  Operations
performed on this dataframe will overwrite the `df` variable with
the results of that operation.  Special consideration is taken for
assignments such as `df['a'] = df.b + 1`.  These are understood
to make column assignments on `df`. By way of example, this command at the bash prompt:

```bash
p.df 'df["c"] = 2 * df.b' 'df.groupby(by="a").c.count()' 'df.reset_index()'
```

is equivalent to the following python snippet:

```python
import pandas as pd
df = pd.read_csv(sys.stdin)
df["c"] = 2 * df.b
df = df.groupby(by="a").c.count()
df = df.reset_index()
df.to_csv(sys.stdout, index=False)
```

Shown below are several examples of how to use the `p.df` tool.  You are encourage
to copy/paste these commands to your bash prompt to see Pandashells in action.

* Show a few rows of an example data set.

  <pre><code><strong>[~]$ p.example_data -d tips | head</strong>
  "total_bill","tip","sex","smoker","day","time","size"
  16.99,1.01,"Female","No","Sun","Dinner",2
  10.34,1.66,"Male","No","Sun","Dinner",3
  21.01,3.5,"Male","No","Sun","Dinner",3
  23.68,3.31,"Male","No","Sun","Dinner",2
  </code></pre>

* Transform the sample data from csv format to table format
  <pre><code><strong>[~]$ p.example_data -d tips | p.df 'df.head()' -o table</strong>
  total_bill   tip     sex smoker  day    time  size
       16.99  1.01  Female     No  Sun  Dinner     2
       10.34  1.66    Male     No  Sun  Dinner     3
       21.01  3.50    Male     No  Sun  Dinner     3
       23.68  3.31    Male     No  Sun  Dinner     2
       24.59  3.61  Female     No  Sun  Dinner     4
 </code></pre>

* Compute statistics for numerical fields in the data set.
  <pre><code><strong>[~]$ p.example_data -d tips | p.df 'df.describe().T' -o table index </strong>
              count       mean       std   min      25%     50%      75%    max
  total_bill    244  19.785943  8.902412  3.07  13.3475  17.795  24.1275  50.81
  tip           244   2.998279  1.383638  1.00   2.0000   2.900   3.5625  10.00
  size          244   2.569672  0.951100  1.00   2.0000   2.000   3.0000   6.00
  </code></pre>

* Find the mean tip broken down by gender and day
  <pre><code><strong>[~]$ p.example_data -d tips | p.df 'df.groupby(by=["sex","day"]).tip.mean()' -o table index</strong>
                    tip
  sex    day
  Female Fri   2.781111
         Sat   2.801786
         Sun   3.367222
         Thur  2.575625
  Male   Fri   2.693000
         Sat   3.083898
         Sun   3.220345
         Thur  2.980333
  </code></pre>

Join files on key fields 
----
Pandashells can join files based on a set of key fields.  This example uses
only one field as a key, but like the pandas merge function on which it is based,
multiple key fields can be used for the join.

* Show poll resultes for the 2008 US presidential election
  <pre><code><strong>[~]$ p.example_data -d election | p.df -o table | head </strong> 
       days state  obama  mccain                           poll
       -305    OH     43      50                      SurveyUSA
       -303    PA     38      46                      Rasmussen
       -298    OR     47      47                      SurveyUSA
       -298    WA     52      43                      SurveyUSA
       -294    AL     29      63                      SurveyUSA
       -294    NY     44      42                    Siena Coll.
       -294    VA     40      52                      SurveyUSA
       -290    NM     41      50                      SurveyUSA
       -290    NY     49      43                      SurveyUSA
  </pre></code>

* Show population and electoral college numbers for states
  <pre><code><strong>[~]$ p.example_data -d electoral_college | p.df -o table | head</strong> 
       state            name  electors  population
          AK          Alaska         3      710000
          AL         Alabama         9     4780000
          AR        Arkansas         6     2916000
          AZ         Arizona        11     6392000
          CA      California        55    37254000
          CO        Colorado         9     5029000
          CT     Connecticut         7     3574000
          DC   Dist. of Col.         3      602000
          DE        Delaware         3      898000
  </pre></code>

* Join poll and electoral-college data  (Note the use of bash <a href="http://tldp.org/LDP/abs/html/process-sub.html">process substitution</a> to specify files to join.)
  <pre><code><strong>[~]$ p.merge &lt(p.example_data -d election) &lt(p.example_data -d electoral_college) --how left --on state | p.df -o table | head</strong> 
       days state  obama  mccain                           poll            name  electors  population
       -252    AK     43      48                      SurveyUSA          Alaska         3      710000
       -213    AK     43      48                      Rasmussen          Alaska         3      710000
       -176    AK     41      50                      Rasmussen          Alaska         3      710000
       -143    AK     41      45                      Rasmussen          Alaska         3      710000
       -112    AK     40      45                      Rasmussen          Alaska         3      710000
        -99    AK     39      44                      Rasmussen          Alaska         3      710000
        -65    AK     35      54            Ivan Moore Research          Alaska         3      710000
        -58    AK     33      64                      Rasmussen          Alaska         3      710000
        -56    AK     39      55                            ARG          Alaska         3      710000
  </code></pre>

Visualization Tools
----
Pandashells provides a number of visualization tools to help you quickly explore your data.
All visualizations are automatically configured to show an interactive plot using the configured
backend (default is TkAgg, but can be configured with the p.config tool).  

As of version 0.2.0 pandashells supports the WebAgg backend for matplotlib. This enables
interactive plots to be shown in a browser.  To run with this option, set configuration with

```bash
p.config --plot_backend WebAgg
```

Note that WebAgg requires that Tornado be installed.  This installation is left up to the user.

The visualizations can also be saved to image files (e.g. .png) or rendered to html.  The html
generated can either be opened directly in the browser to show an interactive plot (using mpld3),
or can be embedded in an existing html file.  The examples below show Pandashells-created png images
along with the command used to generate them.

* Simple xy scatter plots
  <pre><code><strong>[~]$ p.example_data -d tips | p.plot -x total_bill -y tip -s 'o' --title 'Tip Vs Bill'</strong> 
  </code></pre>
  ![Output Image](/images/tips_vs_bill.png?raw=true "xy scatter plot")

* Faceted plots
  <pre><code><strong>[~]$ p.example_data -d tips | p.facet_grid --row smoker --col sex --hue day --map pl.scatter --args total_bill tip --kwargs 'alpha=.2' 's=100'</strong> 
  </code></pre>
  ![Output Image](/images/facet_plot.png?raw=true "facet plot")

* Histograms plots  (Note the use of bash <a href="http://tldp.org/LDP/abs/html/process-sub.html">process substitution</a> to paste two outputs together.)
  
  <pre><code><strong>[~]$ paste &lt(p.rand -t normal -n 10000 | p.df --names normal) &lt(p.rand -t gamma -n 10000 | p.df --names gamma) | p.hist -i table -c normal gamma</strong> 
  </code></pre>
  ![Output Image](/images/hist.png?raw=true "histogram plot")

* Empirical cumulative distribution plots
  
  <pre><code><strong>[~]$ p.rand -t normal -n 500 | p.cdf -c value --names value</strong> 
  </code></pre>
  ![Output Image](/images/cdf_plot.png?raw=true "cdf plot")


Spectral Estimation
---
* Plot a time series over which to compute a spectrum
  <pre><code><strong>[~]$ p.example_data -d sealevel | p.plot -x year -y sealevel_mm</strong> 
  </code></pre>
  ![Output Image](/images/timeseries.png?raw=true "time series plot")

* Plot the spectrum
  <pre><code><strong>[~]$ p.example_data -d sealevel | p.lomb_scargle -t year -y sealevel_mm --interp_exp 3 | p.plot -x period -y amp --xlim 0 1.5 --ylim 0 6.5 --xlabel 'Period years' --ylabel 'Amplitude (mm)' --title 'Global Sea Surface Height Spectrum'</strong> 
  </code></pre>
  ![Output Image](/images/spectrum.png?raw=true "spectrum plot")


Linear Regression
----
Pandashells leverages the excellent Seaborn and Statsmodels libraries to handle
linear regression.

* Quick and dirty fit to a line
  <pre><code><strong>[~]$ p.linspace 0 10 20 | p.df 'df["y_true"] = .2 * df.x' 'df["noise"] = np.random.randn(20)' 'df["y"] = df.y_true + df.noise' --names x | p.regplot -x x -y y</strong> 
  </code></pre>
  ![Output Image](/images/regplot.png?raw=true "regplot plot")


* Multi-variable linear regression
  <pre><code><strong>[~]$p.example_data -d sealevel | p.df 'df["sin"]=np.sin(2*np.pi*df.year)' 'df["cos"]=np.cos(2*np.pi*df.year)' | p.regress -m 'sealevel_mm ~ year + sin + cos'</strong> 


                              OLS Regression Results
  ==============================================================================
  Dep. Variable:            sealevel_mm   R-squared:                       0.961
  Model:                            OLS   Adj. R-squared:                  0.961
  Method:                 Least Squares   F-statistic:                     6442.
  Date:                Mon, 27 Jul 2015   Prob (F-statistic):               0.00
  Time:                        23:28:11   Log-Likelihood:                -2234.0
  No. Observations:                 780   AIC:                             4476.
  Df Residuals:                     776   BIC:                             4495.
  Df Model:                           3
  Covariance Type:            nonrobust
  ==============================================================================
                   coef    std err          t      P>|t|      [95.0% Conf. Int.]
  ------------------------------------------------------------------------------
  Intercept  -6500.1722     47.829   -135.903      0.000     -6594.063 -6406.282
  year           3.2577      0.024    136.513      0.000         3.211     3.305
  sin           -4.6933      0.217    -21.650      0.000        -5.119    -4.268
  cos            1.4061      0.214      6.566      0.000         0.986     1.826
  ==============================================================================
  Omnibus:                        5.332   Durbin-Watson:                   0.709
  Prob(Omnibus):                  0.070   Jarque-Bera (JB):                5.401
  Skew:                          -0.189   Prob(JB):                       0.0672
  Kurtosis:                       2.846   Cond. No.                     6.29e+05
  ==============================================================================

  Warnings:
  [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
  [2] The condition number is large, 6.29e+05. This might indicate that there are
  strong multicollinearity or other numerical problems.
  </code></pre>

Further examples of each tool can be seen by calling it with the -h switch.
You are encouraged to fully explore these examples. They highlight how Pandashells
can be used to significantly improve your efficiency.


Simple Profiling Utility
----
In addition to command-line tools, Pandashells exposes a useful profiling tool
that can be imported into your python code.  The tools is just a simple context
manager that sends timing information to stdout.  The csv-like format of this
output makes it easy to pipe through Pandashells pipelines.  Here are a couple
examples.

### Profiling different parts of your code

Code
```python
import time
from pandashells import Timer
with Timer('entire script'):
    for nn in range(3):
        with Timer('loop {}'.format(nn + 1)):
            time.sleep(.1 * nn)
# Will generate the following output on stdout
#     col1: a string that is easily found with grep
#     col2: the time in seconds (or in hh:mm:ss if pretty=True)
#     col3: the value passed to the 'name' argument of Timer
 ```

  Output
```
__time__,2.6e-05,loop 1
__time__,0.105134,loop 2
__time__,0.204489,loop 3
__time__,0.310102,entire script
```

### Profiling how code scales (measuring "big-O")

Code
```python
import time
from pandashells import Timer

# initialize a list to hold results
results = []

# run a piece of code with different values of the var you want to scale
for nn in range(3):
    # time each iteration
    with Timer('loop {}'.format(nn + 1), silent=True) as timer:
        time.sleep(.1 * nn)
    # add results
    results.append((nn, timer))

# print csv compatible text for further pandashells processing/plotting
print 'nn,seconds'
for nn, timer in results:
    print '{},{}'.format(nn,timer.seconds)
```

___
Projects by [robdmc](https://www.linkedin.com/in/robdecarvalho).
* [Pandashells](https://github.com/robdmc/pandashells) Pandas at the bash command line
* [Consecution](https://github.com/robdmc/consecution) Pipeline abstraction for Python
* [Behold](https://github.com/robdmc/behold) Helping debug large Python projects
* [Crontabs](https://github.com/robdmc/crontabs) Simple scheduling library for Python scripts
* [Switchenv](https://github.com/robdmc/switchenv) Manager for bash environments
