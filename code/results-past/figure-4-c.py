"""
fully tested with feature change, norm-feature change, feature sloc, norm-feature sloc
"""
import re
import os
import matplotlib.pyplot as plt
import re
import numpy as np
import math
from scipy.stats.stats import kendalltau
import scipy
from matplotlib.patches import Rectangle
from  scipy import stats



import seaborn as sns
import pandas as pd
sns.set(font_scale = 1.2)
fig = plt.figure()
ax = fig.add_subplot(111)


PROJECTS_LIST = "../../info/settings-project.txt"

RESULT_PATH="../../data/complexity-and-change-data/"

PROJECTS = {}
correl_feature = {}

styles=['-', '--','-.',':']
colors = ['r', 'g','b','y']
styles=["-", "--","-.", ":", "-", "--","-.", ":"]
marks=["^", "d", "o", "v", "p", "s", "<", ">"]
#marks_size=[15, 17, 10, 15, 17, 10, 12,15]
marks_size=[15, 17, 10, 15, 17, 10, 12,15]
marker_color=['#0F52BA','#ff7518','#6CA939','#e34234','#756bb1','brown','#c994c7', '#636363']

gap = [5,5,3,4,4,3]

def list_projects():
  fr = open(PROJECTS_LIST,"r")
  lines = fr.readlines()
  fr.close()
  projects = []
  c = 0
  for line in lines:
  
    c+=1
   # if c>2:
   #   break

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
  
  global tot
 
  X = []
  Y = []
  for project in PROJECTS: 
    list_indexes(feature, "checkstyle")  
      
    fr = open(RESULT_PATH+project+".txt")
    line =  fr.readline() ## header
    lines = fr.readlines()
    fr.close()
    
    for line in lines:
        
      line = line.strip()      
      data = re.findall("[^\t]+",line)
      age = int(data[0])
       

      if apply_age_restriction == 1 and age < age_restriction:
        continue
    
      method =  data[len(data)-1]
      
        
      feature_values = re.findall("[^,]+",data[feature_index])
      sloc_values = re.findall("[^,]+",data[sloc_index])
      date_values = re.findall("[^,]+",data[date_index])
      diff_values = re.findall("[^,]+",data[diff_index])
      track = 0  
      
      for i in range(1, len(diff_values)):

        if int(date_values[i]) > age_restriction: ## change not within  time          
          break
        
        if int(diff_values[i]) == 0: ## no change in content      
          continue
        
        track = 1
        
        feature_value = float(feature_values[i-1]) ## current change happened because of the previous state  
        sloc = float(sloc_values[i-1])
      
        
        if sloc_normalized == 1:
          feature_value = 100.0 * (feature_value/sloc)      
          if feature_value == 200.0:
            tot += 1
        X.append(sloc)
        Y.append(feature_value)
     
         
      if track == 0: ## there was no change
        feature_value = float(feature_values[0]) 
        sloc = float(sloc_values[0])
                
        if sloc_normalized == 1:
 
          feature_value = 100.0 * (feature_value/sloc)        
          if feature_value == 200.0:
            tot += 1
        
        X.append(sloc)
        Y.append(feature_value)



  print tot
  return X,Y

def list_indexes(feature, project):

  global feature_index
  global date_index
  global diff_index
  global addition_index
  global edit_index
  global sloc_index
  feature_index = find_index(feature, project)
  sloc_index = find_index("SLOCStandard", project)
  date_index = find_index("ChangeDates", project)
  diff_index = find_index("DiffSizes", project)
  addition_index = find_index("NewAdditions", project)
  edit_index = find_index("EditDistances", project)


def draw_scatter(X, Y):
  plt.scatter(X, Y, color ="#0F52BA")
  #ax.set_ylim(0, 1)
  #ax.set_xlim(1, 100)
  plt.xlabel("SLOC", fontsize = 18)
  plt.ylabel("Normalized McCabe",fontsize = 18)

 # ax.set_yscale('log')
  ax.set_xscale('log')
#  plt.legend(("All","Successful"),loc=0,fontsize=20)

  for label in ax.get_xticklabels():
    label.set_fontsize(18)
  for label in ax.get_yticklabels():
    label.set_fontsize(16)
#  plt.grid(True)
#  plt.title(PROJECT,fontsize=20)
  plt.tight_layout() 
  plt.show()


if __name__ == "__main__":

  
  global feature 
  global age_restriction
  global changeTypes
  global risks
  global STATS
  global CONFOUND
  global tot
  tot = 0
  apply_age_restriction = 1
  age_restriction = 730
  sloc_normalized = 1
  all_features =['McCabe']
  list_projects()
  for feature in all_features:
    print feature  
    X, Y = parse_data()

  draw_scatter(X,Y)

