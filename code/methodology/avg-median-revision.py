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
STATS = {}
METHODS = {}
total_methods = 0
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
  global total_methods

  for project in PROJECTS:
    STATS[project]=[]	
    index_day = find_index("ChangeDates", project)
    index_diff = find_index("DiffSizes", project)

    fr = open(RESULT_PATH+project+".txt")
    line =  fr.readline() ## header
    lines = fr.readlines()
    fr.close()

    METHODS[project] = len(lines)
    total_methods += len(lines)

    for line in lines:
      line = line.strip()
      data = re.findall("[^\t]+",line)
      dates = re.findall("[^,]+",data[index_day])
      diffs = re.findall("[^,]+",data[index_diff])
      ### index 0 is for introduction and should be ignored
      count = 0
      for i in range(1,len(dates)):

        #if int(diffs[i]) > 0: ## was not just filerename or moved
        count+=1
      STATS[project].append(count)	  
       

def stats():
  for entry in sorted(METHODS.items(), key=lambda x: x[1], reverse =  True):
    project = entry [0]
   # hadoop              &  24,112 &  70,524 &  10,800 &  &  \\
    if len(str(entry[1]))<4:
      methods = entry[1]
    else:
      methods = str(entry[1])[:len(str(entry[1]))-3]+","+ str(entry[1])[len(str(entry[1]))-3:] 
    print project, "&", methods, "&", round(np.mean(STATS[project]),1), "&", round(np.median(STATS[project]),1), "&", round(np.max(STATS[project]),1), "&", round(np.percentile(STATS[project],95),1), "\\\\"

  print "total methods = ", total_methods
if __name__ == "__main__":
      
  list_projects()
  parse_change()
  stats()
  #print  STATS['elasticsearch']

