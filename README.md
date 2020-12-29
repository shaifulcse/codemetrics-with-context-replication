# codemetrics-with-context-replication

### Complexity and Change Data

The `info/settings-project.txt` file contains: project name checkoutDate  and snapshot for checkout (for all the 47 projects).

### Complexity and Change Data

The `data/complexity-and-change-data` directory contains measurements for all the 47 Java projects. 
The first line (header) shows the metrics' names (columns are separated by tab). For each metric measurement, there can be multiple values because we captured the complete evolution history of each method. 

McCabe values 5,6,7 means at the introduction (when the method was first pushed), the McCabe was 5. Then after a change, it became 6, and then 7 (latest).   

But for change values (such as ChangeDates), the first value is always 0. It means the method was introduced that day. The first value is 0 for other change indicators as well, because the method was introduced, not modified.  


### Replication
Here we describe how to reproduce the results of the paper in each section.

#### Prerequisites

`Ubuntu 18.04`
`Python 2.7`
`matplotlib`
`scipy`
`seaborn`
`sklearn`
`numpy`


#### Related work

##### Confound factor

`cd code/RL/`

`python NBDvsReadability.py`

##### Normalization
For both graphs:

`cd code/RL/`

`python change_transformation.py`

#### Methodology

##### Table 1

`cd code/methodology/`

`python avg-median-revision.py`

##### Age Normalization graph

`cd code/methodology/`

`python  combiner.py`

#### Results (Past)

#####  Code metrics and #Revisions

`cd code/results-past/`

`python  figure-3-a.py`

#####  SLOC and change indicators

`cd code/results-past/`

`python  figure-3-b.py`

#####  Code metrics and SLOC

`cd code/results-past/`

`python  figure-3-c.py`

#####  Normalized metrics and #Revisions

`cd code/results-past/`

`python  figure-4-a.py`

#####  Normalized metrics and SLOC

`cd code/results-past/`

`python  figure-4-b.py`

##### Normalized McCabe against SLOC

`cd code/results-past/`

`python  figure-4-c.py`


#### Regression

##### Figure 6 (a)

`cd code/regression/`

`python  figure-6-a.py`

##### Figure 6 (b)

`cd code/regression/`

`python  figure-6-b.py`

##### Figure 6 (c)

`cd code/regression/`

`python  figure-6-c.py`




