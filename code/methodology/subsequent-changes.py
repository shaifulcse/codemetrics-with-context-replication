import re
import os
import matplotlib.pyplot as plt
import re
import numpy as np
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
from matplotlib.patches import Rectangle

##############

#This program is tested 

#####################

fig = plt.figure()
ax = fig.add_subplot(111)

PROJECTS_LIST = "../../info/settings-project.txt"

RESULT_PATH="../../data/complexity-and-change-data/"

PROJECTS = {}
DATES = {}
MAX = 0
def list_projects():
  fr = open(PROJECTS_LIST,"r")
  lines = fr.readlines()
  fr.close()
  projects = []
  c = 0
  for line in lines:
  
    c+=1
    #if c>2:
    #  break
    if len(line)<5:
      break 
    line = line.strip()
    data = re.findall("[^\t]+",line)
    if data[0] not in PROJECTS:
      PROJECTS[data[0]]=1
      ### to help step2

   

def find_index(feature, project):
  fr = open(RESULT_PATH+project+".txt")
  line =  fr.readline() ## header
  line = line.strip()
  data = re.findall("[^\t]+",line)
  for i in range(len(data)):
    if data[i] == feature:
      return i

def parse_change():

  for project in PROJECTS:
    index_day = find_index("ChangeDates", project)
    index_diff = find_index("DiffSizes", project)

    fr = open(RESULT_PATH+project+".txt")
    line =  fr.readline() ## header
    lines = fr.readlines()
    fr.close()
    
    for line in lines:
      line = line.strip()
      data = re.findall("[^\t]+",line)
      dates = re.findall("[^,]+",data[index_day])
      diffs = re.findall("[^,]+",data[index_diff])
      age = int(data[0])
      ### index 0 is for introduction and should be ignored
      
      prev_date = 0
      for i in range(1,len(dates)):
        date = int(dates[i])
        if int(diffs[i]) > 0: ## was not just filerename or moved
          changeTime = date - prev_date
          prev_date = date
          if changeTime not in DATES:
                        
            DATES[changeTime] = 1
          else:
            DATES[changeTime] += 1

       
def draw_graph(cdf):

  line=(plt.plot(range(0, len(cdf)),cdf))
  plt.setp(line,color='b', linewidth=4,ls='-')

  #ax.set_ylim(0, 1)
  #ax.set_xlim(1, 12)
  plt.xlabel("# Days between change commit",fontsize=20)
  plt.ylabel("CDF",fontsize=20)

#  plt.legend(("Broke rule","Followed Rule"),loc=0,fontsize=20)

  plt.xscale("log")

  for label in ax.get_xticklabels():
    label.set_fontsize(18)
  for label in ax.get_yticklabels():
    label.set_fontsize(18)

  currentAxis = plt.gca()
  currentAxis.add_patch(Rectangle((730 , 0.0), 0, 0.9, fill=False, color = 'red', linewidth = 3))

  plt.grid(True)
  plt.show()

def find_max():
  global MAX
  for date in DATES:
    
    if MAX<int(date):
      MAX = int(date)

def build_cdf():

  total = 0.0
  for date in DATES:
    total += DATES[date]
  
  find_max()
  
  cdf = [0.0]*(MAX+1)
  ccdf = [0.0]*(MAX+1)
  prev = 0.0

  for date in range(MAX+1):

    if date not in DATES:
      prob = 0.0
    else:
      prob = DATES[date]/total

    cdf[date] += prob + prev
    ccdf[date] = 1 - cdf[date]
    prev =  cdf[date]
 
  return cdf

def write(cdf):
  fw = open("combined-data.csv","a")
  fw.write("sub-changes\t")
  for i in range(len(cdf)):
    fw.write(str(cdf[i])+"\t")
  fw.write("\n")
  fw.close()
  
if __name__ == "__main__":
      
  list_projects()
#  index_day = find_index("ChangeDates", "checkstyle")
#  index_diff = find_index("DiffSizes", "checkstyle")
  parse_change()
  cdf = build_cdf()
  draw_graph(cdf)
  write(cdf)
  
