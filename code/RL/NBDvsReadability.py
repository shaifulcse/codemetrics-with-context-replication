import re
import os
import matplotlib.pyplot as plt
import re
import numpy as np
from  scipy import stats

fig = plt.figure()
ax = fig.add_subplot(111)

PATH="../../data/previous-work/replication-icsme-readability/icsme19/replicationpackage/snippets.csv"
MAX=0

sloc_no_rule = []
sloc_rule = []

def parse_data():
  global MAX
  fr = open(PATH,"r")
  line = fr.readline()
  data = re.findall("[^,]+",line)
  lines = fr.readlines()
  for line in lines:
    data = re.findall("[^,]+",line)
    if (data[3])=="yes":
      sloc_rule.append(int(data[4]))
    else:
      sloc_no_rule.append(int(data[4]))

    if(MAX<int(data[4])):
      MAX = int(data[4]) 

  fr.close()

def draw_graph(sloc_no_rule, sloc_rule):
  print no_rule
  print rule
  
  line=(plt.plot(range(len(sloc_no_rule)),sloc_no_rule))
  plt.setp(line,color='r', linewidth=4,ls='-')

  
  line=(plt.plot(range(len(sloc_rule)),sloc_rule))
  plt.setp(line,color='b', linewidth=4,ls='--')

  ax.set_ylim(0, 1)
  ax.set_xlim(9, MAX)
  plt.xlabel("SLOC",fontsize=20)
  plt.ylabel("CDF",fontsize=20)

  plt.legend(("Broke rule","Followed Rule"),loc=0,fontsize=20)

  for label in ax.get_xticklabels():
    label.set_fontsize(18)
  for label in ax.get_yticklabels():
    label.set_fontsize(18)
  plt.grid(True)
  plt.show()

def cdf_builder(ls):
  pr=[0.0]*(MAX+1)
  sm=0
  total = len(ls)
  
  for i in ls:
    pr[i] += 1  
  for i in range(len(pr)):
    pr[i] = sm + (pr[i] / total)
    sm =  pr[i]
  return pr   	  	

if __name__ == "__main__":

   
  parse_data()
  no_rule = cdf_builder(sloc_no_rule)
  rule = cdf_builder(sloc_rule)  
  draw_graph(no_rule, rule)
