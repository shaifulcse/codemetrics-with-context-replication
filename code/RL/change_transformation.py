import re
import os
import matplotlib.pyplot as plt
import re
import numpy as np
import math
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
import scipy
from matplotlib.patches import Rectangle
from  scipy import stats
##############

#This program is for 4 types of change normalization, not #for feature normalization

#####################

fig = plt.figure()
ax = fig.add_subplot(111)

PROJECTS_LIST = "../../info/settings-project.txt"

RESULT_PATH="../../data/complexity-and-change-data/"

styles=['-', '--','-.',':']
colors = ['r', 'g','b','y']

PROJECTS = {}
STATS = {}
MAX = 0
TRANSFORMED = {}
GLOBAL_KEYS = {}
ALL_DIST = []

def list_projects():
  fr = open(PROJECTS_LIST,"r")
  lines = fr.readlines()
  fr.close()
  projects = []
  c = 0
  for line in lines:
  
    c+=1
    #if c>5:
    #  break
    if len(line)<5:## for blank lines
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


def parse_data():

  for project in PROJECTS:

    feature_index = find_index(feature, project)
    date_index = find_index("ChangeDates", project)
    realChange_index = find_index("DiffSizes", project)

    STATS[project]={}

    fr = open(RESULT_PATH+project+".txt")
    line =  fr.readline() ## header
    lines = fr.readlines()
    fr.close()
    
    for line in lines:
      line = line.strip()
      data = re.findall("[^\t]+",line)
      values = re.findall("[^,]+",data[feature_index])
      date_values = re.findall("[^,]+",data[date_index])
      realChage_values = re.findall("[^,]+",data[realChange_index])
      age = int(data[0])

      if apply_age_restriction == 1 and age <age_restriction:
        continue

      sum = calculate_sum(values, date_values, realChage_values)
   
      if sum not in STATS[project]:
        STATS[project][sum] = 1
      else:
        STATS[project][sum] += 1


def calculate_sum(values, date_values,realChage_values):
  sum =0

  for i in range(1, len(values)): ## ignore intro

    if apply_age_restriction == 1  and int(date_values[i])>age_restriction: ## normalization with age
      break

    if int(realChage_values[i])==0: ## no content change
      continue 

    if(feature == "ChangeDates"):       
      sum +=1
    else:
      sum +=int(values[i]) 
  return sum
       
def draw_graph(dic):

  graph_index=0; 
  for project in dic:
    
    X,Y = build_cdf(dic[project])
    line=(plt.plot(X,Y))
    plt.setp(line,color=colors[graph_index%len(colors)], linewidth=2,ls=styles[graph_index%len(styles)])
    graph_index+=1    
  #ax.set_ylim(0, 1)
  #ax.set_xlim(0, 100)
  plt.xlabel("#Revisions",fontsize=20)
  plt.ylabel("CDF",fontsize=20)
  
#  plt.legend(("Broke rule","Followed Rule"),loc=0,fontsize=20)

  plt.xscale("log")

  for label in ax.get_xticklabels():
    label.set_fontsize(20)
  for label in ax.get_yticklabels():
    label.set_fontsize(20)
  plt.grid(True)
  plt.tight_layout() 
  plt.show()



def build_cdf(dic):
 
  X = []
  Y = [] 
  total = 0.0
  prev = 0.0

  for key in dic:
    total += dic[key]

  for key in sorted(dic):

    X.append(key)

#    if key not in dic:
#      dic[key] = 0.0

    prob = dic[key]/total
    Y.append(prob + prev)
    prev =  prob + prev
  return X,Y  


     
def toLogNormal():
  LOG_STATS = {}
  for project in STATS:
    LOG_STATS[project]={}
    for key in STATS[project]:
      logKey = math.log(1+key,10) ## 1 to avoid math error     
      LOG_STATS[project][logKey] = STATS[project][key]
 
  for project in LOG_STATS:

    TRANSFORMED[project] = {}
      
    avg = average(LOG_STATS[project])
    std = stdev(LOG_STATS[project])
     
    for key in sorted(LOG_STATS[project]):
      value = (key - avg)/std
      TRANSFORMED[project][value]=LOG_STATS[project][key]
  

def stdev(dic):
  ls = []
  for key in dic:
    for i in range(dic[key]):
      ls.append(key)

  return np.std(ls)

def average(dic):

  total = 0.0
  sum = 0.0
  for key in dic:
    sum += (key*dic[key])
    total += dic[key]

  return sum/total  


if __name__ == "__main__":

  global  log_normal_transform
  global feature 
  global age_restriction
  apply_age_restriction = 0
  age_restriction = 730
  feature = "ChangeDates" ### changeDates for #revisions
  list_projects()
  
  parse_data()
  
  toLogNormal()
  
  draw_graph(STATS)
  draw_graph(TRANSFORMED)
  
  
  
