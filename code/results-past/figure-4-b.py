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

styles=["-", "--","-.", ":", "-", "--","-.", ":"]
marks=["^", "d", "o", "v", "p", "s", "*", ">"]
#marks_size=[15, 17, 10, 15, 17, 10, 12,15]
marks_size=[12, 12, 12, 12, 12, 12, 18, 20]
marker_color=['#0F52BA','#ff7518','#6CA939','#e34234','#756bb1','brown','#c994c7', '#636363']
gap = [3,5,3,4,3,2,4,5,3]


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
  global STATS
  
  for project in PROJECTS: 
    list_indexes(feature, "checkstyle")  
    STATS[project]={}
    
    if project not in CONFOUND:
      CONFOUND[project] ={}
      CONFOUND[project]['sloc']=[]
      CONFOUND[project]['feature']=[]
      
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
      
      if method not in STATS[project]:
        STATS[project][method]={}
        
      feature_values = re.findall("[^,]+",data[feature_index])
      sloc_values = re.findall("[^,]+",data[sloc_index])
      date_values = re.findall("[^,]+",data[date_index])
      diff_values = re.findall("[^,]+",data[diff_index])
      addition_values = re.findall("[^,]+",data[addition_index])
      edit_values = re.findall("[^,]+",data[edit_index])
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
     
        CONFOUND[project]['sloc'].append(sloc)
        CONFOUND[project]['feature'].append(feature_value)
     
        if feature_value not in  STATS[project][method]:
          STATS[project][method][feature_value]=build_dic()  
        update_stats(project, method, feature_value, 1, int(addition_values[i]), int(diff_values[i]), int(edit_values[i]))
         
      if track == 0: ## there was no change
        feature_value = float(feature_values[0]) 
        sloc = float(sloc_values[0])
                
        if sloc_normalized == 1:
          feature_value = 100.0 * (feature_value/sloc)        
        
        CONFOUND[project]['sloc'].append(sloc)
        CONFOUND[project]['feature'].append(feature_value)       
    
        if feature_value not in STATS[project][method]:
          
          STATS[project][method][feature_value]=build_dic()  
        update_stats(project, method, feature_value, 0, 0, 0, 0)          
  #print STATS['ant']['5216.json']
def update_stats(project, method, feature_value, rev, add, diff, edit):
#  print project, method   
  STATS[project][method][feature_value][changeTypes[0]] += rev ### 
  STATS[project][method][feature_value][changeTypes[1]] += add
  STATS[project][method][feature_value][changeTypes[2]] += diff
  STATS[project][method][feature_value][changeTypes[3]] += edit
    

def build_dic():
  dic = {}
  for t in changeTypes:      
    dic[t]=0
  return dic
   
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

def correlation():
   
  for project in STATS:
    for type in changeTypes:     
      if type != changeTypes[0]:
        continue      
      X=[]
      Y=[]      
      
      for method in STATS[project]:

        for feature_value in STATS[project][method]:
          
          X.append(feature_value)      
          Y.append(STATS[project][method][feature_value][type])
            
            
      #print project, type, X, Y    
      cr = kendalltau(X, Y)    
      con = kendalltau(CONFOUND[project]['sloc'], CONFOUND[project]['feature'])
     
      correl_feature[feature].append(float(con[0]))    
          
    #  print project, type, cr[0], con[0]   


def build_cdf(ls):

  X = []
  Y = [] 
  prev = 0.0
  total = len(ls)
  dic = {} 
  
  for key in ls:
    if key not in dic:
      dic[key] = 0.0
    dic[key] += 1.0

  tracked = {}
  for key in sorted(ls):

    if key in tracked:
      continue
    tracked[key] = 1 

    X.append(key)
    prob = dic[key]/total
    Y.append(prob + prev)
    prev =  prob + prev
    
  return X,Y  
  
  

def draw_graph():
  index = 0
  #for type in   changeTypes:    
  for feature in all_features:

    X,Y = build_cdf(correl_feature[feature])
            
    
    line=(plt.plot(X,Y))
    
    plt.setp(line, linewidth=1,ls=styles[index], marker=marks[index], 
             markerfacecolor=marker_color[index], markersize = marks_size[index], color=marker_color[index],markevery=gap[index])
    index += 1
  plt.legend((legends),loc=0,fontsize=14)
  plt.xlabel("Correlation",fontsize=20)
  plt.ylabel("CDF",fontsize=18) 

  plt.xticks(rotation=25)
  for label in ax.get_xticklabels():
    label.set_fontsize(19)
  for label in ax.get_yticklabels():
    label.set_fontsize(18)

  plt.tight_layout() 
  plt.show()

if __name__ == "__main__":

  
  global feature 
  global age_restriction
  global changeTypes
  global risks
  global STATS
  global CONFOUNDtotalFanOut
  
  apply_age_restriction = 1
  age_restriction = 730
  sloc_normalized = 1
  changeTypes =["#Revisions", "NewAdditions", "DiffSizes", "EditDistances"] 
  ### will change based on feature 
  #all_features = ['McCabe', 'IndentSTD','totalFanOut','Readability']
  all_features =['McCabe','Mcclure','MaximumBlockDepth', 'IndentSTD','totalFanOut', 'Readability',  'MaintainabilityIndex']
  legends = ['McCabe','McClure','NBD', 'IndentSTD','totalFanOut', 'Readability', 'MIndex']
  #legends = ['McCabe', 'IndentSTD','totalFanOut','Readability']
  #all_features = ['McCabe','Mcclure']
  
  list_projects()
  
  for feature in all_features:
    print feature
    
    STATS = {}
    CONFOUND ={}    
    correl_feature[feature] = []

    parse_data()
    correlation()
    
  draw_graph()  

