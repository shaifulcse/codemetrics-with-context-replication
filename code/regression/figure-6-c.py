"""
"""
import re
from  scipy import stats
from sklearn import linear_model
import regressionModule
import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sns
import pandas as pd
import matplotlib.patches as patches

sns.set(font_scale = 1.2)
fig = plt.figure()
ax = fig.add_subplot(111)


styles=["-", "--","-.", ":", "-", "--","-.", ":"]
marks=["^", "d", "o", "v", "p", "s", "*", ">"]
#marks_size=[15, 17, 10, 15, 17, 10, 12,15]
marks_size=[12, 12, 12, 12, 12, 12, 15, 20]
marker_color=['#0F52BA','#ff7518','#6CA939','#e34234','#756bb1','brown','#c994c7', '#636363']
gap = [3,5,3,4,3,2,4,5,3]

PROJECTS_LIST = "../../info/settings-project.txt"

RESULT_PATH="../../data/complexity-and-change-data/"
#RESULT_PATH="/home/shaiful/research/software-evolution/result/static-analysis/source-code/selected-features-corrected/"

PROJECTS = {}
STATS = {}
feature_improvement = {}


def list_projects():
  fr = open(PROJECTS_LIST,"r")
  lines = fr.readlines()
  fr.close()
  projects = []
  c = 0
  for line in lines:
  
    line = line.strip()
    data = line.split('\t')
    if data[0] not in PROJECTS:
      PROJECTS[data[0]]=1

   
def find_index(feature, project):
  fr = open(RESULT_PATH+project+".txt")
  line =  fr.readline() ## header
  line = line.strip()
  data = line.split('\t')
  for i in range(len(data)):
    if data[i] == feature:
      return i


def parse_data():
  global STATS
  for project in PROJECTS: 
    list_indexes(feature,"checkstyle")    
    STATS[project]={}
    
    fr = open(RESULT_PATH+project+".txt")
    line =  fr.readline() ## header
    lines = fr.readlines()
    fr.close()
    
    for line in lines:
      line = line.strip()
      data = line.split('\t')      
      age = int(data[0])
       
      if apply_age_restriction == 1 and age < age_restriction:
        continue
          
      method =  data[len(data)-1]

      if method not in STATS[project]:
        STATS[project][method]={}

      feature_values = data[feature_index].split(',')       
      sloc_values = data[sloc_index].split(',')
      date_values = data[date_index].split(',')
      diff_values = data[diff_index].split(',')
      addition_values = data[addition_index].split(',')
      edit_values = data[edit_index].split(',')
      
     
      track = 0  
      for i in range(1, len(diff_values)):
        
        if int(date_values[i]) > age_restriction: ## change not within  time        
          break
        
        if int(diff_values[i]) == 0: ## no change in content        
          continue
             
        track = 1
        feature_value = float(feature_values[i-1]) ## current change happened because of the previous state    
        sloc = float(sloc_values[i-1])
        
        if check_group(sloc) == 0:
          continue        
           
        joint_feature = str(sloc)+"-"+str(feature_value)
        
        if joint_feature not in STATS[project][method]:
          STATS[project][method][joint_feature] = build_dic()

        update_stats(project, method, joint_feature, 1, int(addition_values[i]), int(diff_values[i]),
                     int(edit_values[i]))
        
      if track == 0: ## there was no change
        feature_value = float(feature_values[0]) ##         
        sloc = float(sloc_values[0])      
        
        if check_group(sloc) == 0:
          continue
        
        joint_feature = str(sloc)+"-"+str(feature_value)
       
        if joint_feature not in STATS[project][method]:
          STATS[project][method][joint_feature] = build_dic()        
               
        update_stats(project, method, joint_feature, 0, 0, 0,
                     0)



def update_stats(project, method, joint_feature, rev, add, diff, edit):
  
  STATS[project][method][joint_feature][changeTypes[0]] += rev ## one revision
  STATS[project][method][joint_feature][changeTypes[1]] += add 
  STATS[project][method][joint_feature][changeTypes[2]] += diff
  STATS[project][method][joint_feature][changeTypes[3]] += edit
  
def build_dic():
  dic ={}
  for type in changeTypes:
    dic[type] = 0.0
  return dic  

def list_indexes(feature,project):

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


  
def regression(f):
  
  #notTested = 0
   
  for project in STATS:
    #if project != 'hadoop':
    #  continue
    sloc = []
    feature= []
    change = []         
    
    for method in STATS[project]:
      for joint in STATS[project][method]:
        data = joint.split("-")
       
        slc = float(data[0])

        if '--' in joint:
          ft = float(data[2])
        else:
          ft = float(data[1])

        sloc.append(slc)
        feature.append(ft)
      
        change.append(STATS[project][method][joint][type])

    
    
    if testSampleLimit == 1:
      if len(sloc)<sampleLimit:
        #notTested += 1
        continue
    
    clf = linear_model.LinearRegression()

    x = np.array(zip(sloc))
    y =np.array(zip(change))
    clf.fit(x, y)
    p_values = regressionModule.calculte_p_values(x,y, clf)
    sloc_score = clf.score(x,y)
    
    x = np.array(zip(sloc,feature))
    y =np.array(zip(change))     
    clf.fit(x, y)     
    p_values = regressionModule.calculte_p_values(x,y, clf)
    
    joint_score = clf.score(x,y)
    
    #print project, "with feature", joint_score
    improvement = (joint_score-sloc_score)*100/sloc_score

    if check_pValue == 1:
      if (float(p_values[2]) > 0.05):
        improvement= 0.0
    feature_improvement[f].append(improvement)
    #write_for_R(sloc, feature, change)
    #print "improvement",improvement
    #print "\n"
  #print "Low sample: ",notTested

"""  
def write_for_R(sloc, feature, change):
  fw = open("R.csv","w")
  fw.write("sloc,feature,change\n")
  for i in range(len(sloc)):
    fw.write(str(sloc[i])+","+str(feature[i])+","+str(change[i])+"\n") 
  fw.close()
"""
   
def draw_graph():
  index = 0
  for feature in  all_features:    
   # if feature != 'IndentSTD':
   #   continue
       
    #print feature
    X,Y = build_cdf(feature_improvement[feature])
   
    line=(plt.plot(X,Y))
    
    plt.setp(line, linewidth=3,ls=styles[index], marker=marks[index],

             markerfacecolor=marker_color[index], markersize = marks_size[index], color=marker_color[index],markevery=gap[index])
    index += 1
    
    
  plt.legend((legends),loc=0,fontsize=14)
  plt.xlabel("Improvement %",fontsize=18)
  plt.ylabel("CDF",fontsize=18)  
  plt.xscale("log")
  for label in ax.get_xticklabels():
    label.set_fontsize(18)
  for label in ax.get_yticklabels():
    label.set_fontsize(18)
  plt.grid(True)  
  ax.set_ylim(0, 1.10)



  plt.tight_layout() 
  plt.show()


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

def write_for_effsize():
  fw = open("improvement_data.csv","w")
  
  for f in feature_improvement:
    fw.write(f+"\t")
   # print feature_improvement[f]
    for v in feature_improvement[f]:
      fw.write(str(v)+"\t")
    fw.write("\n")
  fw.close()
  

def check_group(size):
  return 1 ### for all, no filtering
  if size <=33:
    return 0
  return 1 


    
if __name__ == "__main__":

  
  global feature 
  global age_restriction
  global changeTypes
  global type
  global check_pValue
  global testSampleLimit
  global sampleLimit
  global legends

  testSampleLimit = 1
  sampleLimit = 30    ## don't test if #samples is less than 30, because it won't make sense statistically

  check_pValue = 1 
   
  apply_age_restriction = 1
  age_restriction = 730
    
  changeTypes =["#Revisions", "NewAdditions", "DiffSizes", "EditDistances"] 

  type = changeTypes[3]  

  all_features =['McCabe','Mcclure','MaximumBlockDepth', 'IndentSTD','totalFanOut', 'Readability',  'MaintainabilityIndex']

  legends = ['McCabe','McClure','NBD', 'IndentSTD','totalFanOut', 'Readability', 'MIndex']

  #all_features =['MaintainabilityIndex']
  #legends = ['MIndex']
  list_projects()


  for feature in all_features:
    print feature  
    feature_improvement[feature] = []  
    parse_data()
    regression(feature)
    
  draw_graph()
  write_for_effsize()  

