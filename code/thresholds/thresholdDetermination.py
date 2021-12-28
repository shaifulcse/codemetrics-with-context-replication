import re
import os
import matplotlib.pyplot as plt
import re
import numpy as np
from  scipy import stats
from matplotlib.patches import Rectangle

fig = plt.figure()
ax = fig.add_subplot(111)

PROJECTS_LIST = "../../info/settings-project.txt"

RESULT_PATH="../../data/complexity-and-change-data/"

PROJECTS = {}
INDEXES = {}
FEATURE_VALUE = {}
DIST ={}

def list_projects():
  fr = open(PROJECTS_LIST,"r")
  lines = fr.readlines()
  fr.close()
  projects = []
  c = 0
  for line in lines:
  
    c+=1
  #  if c>2:
  #    break
    if len(line)<5:
      break 
    line = line.strip()
    data = re.findall("[^\t]+",line)
    if data[0] not in PROJECTS:
      PROJECTS[data[0]]={}
      ### to help step2
      PROJECTS[data[0]]['tot_size']=0.0 
   

def find_index(feature, project):
  fr = open(RESULT_PATH+project+".txt")
  line =  fr.readline() ## header
  line = line.strip()
  data = re.findall("[^\t]+",line)
  for i in range(len(data)):
    if data[i] == feature:
      return i

def find_indexes(feature):

  INDEXES['sloc'] = find_index("SLOCStandard","checkstyle")
  INDEXES[feature] =   find_index(feature,"checkstyle")


def calculate_thresholds():
  step1()
  step2()
  step3() 
  step4()
  step5()
  step6()

def step1():

  for project in PROJECTS:
    fr = open(RESULT_PATH+project+".txt")
    line =  fr.readline() ## header
    lines = fr.readlines()
    fr.close()
    
    for line in lines:
      line = line.strip()
      data = re.findall("[^\t]+",line)
      method = data[len(data)-1]
      sloc =re.findall("[^,]+", data[INDEXES['sloc']]) 

      if intro_or_end == 0:
        version = 0
      else:
        version = len(sloc)-1
      
      if(discardSmall == 1 and int(sloc[version]) <= 4):
        continue

      PROJECTS[project][method]={}
      PROJECTS[project][method]['sloc'] = int(sloc[version])
      PROJECTS[project]['tot_size'] += int(sloc[version])
   
      value =re.findall("[^,]+", data[INDEXES[feature_to_look]]) 
      PROJECTS[project][method][feature_to_look] = float(value[version])


def step2():

  for project in PROJECTS:


    for method in  PROJECTS[project]:
      if method == 'tot_size':
        continue
       
      PROJECTS[project][method]['weight'] = PROJECTS[project][method]['sloc'] / PROJECTS[project]['tot_size'] 
  

def step3():
  
  for project in PROJECTS:

    FEATURE_VALUE[project] = {}
    
    for method in  PROJECTS[project]:
      if method == 'tot_size':
        continue
      feature_value = PROJECTS[project][method][feature_to_look]
      if feature_value not in FEATURE_VALUE[project] :
        FEATURE_VALUE[project][feature_value] = PROJECTS[project][method]['weight']

      else:
        FEATURE_VALUE[project][feature_value] += PROJECTS[project][method]['weight']

def step4():
  for project in FEATURE_VALUE:
    for feature_value in FEATURE_VALUE[project]:
      FEATURE_VALUE[project][feature_value] /=  len(PROJECTS) 

def step5():

  for project in FEATURE_VALUE:
    for feature_value in FEATURE_VALUE[project]:
      if feature_value not in DIST:
        DIST[feature_value] = FEATURE_VALUE[project][feature_value]
      else:
        DIST[feature_value] += FEATURE_VALUE[project][feature_value]

def step6():

  track = 0
  percent = 0.0
  low = 0
  medium = 0
  high = 0
  bound = 0

  for value in sorted(DIST):

    percent += DIST[value]
    print bound, value, percent
    
    if percent>0.7 and track == 0:
      low =  bound
      track  = 1

    if percent > 0.8 and track ==1:
      track = 2
      medium  = bound

    if percent > 0.9:
      high =  bound
      break      
     
    bound = value

  print "###############################"
  print feature_to_look
  print "low: <="+str(low)
  print "medium: > "+str(low)+" && <= "+str(medium)
  print "high: > "+str(medium)+" && <="+str(high)
  print "Very high: > "+str(high) 
  
  print "*** \n\n Note that the less than greater than relation is from the originial paper, not the same as Kamei 2016"
  print "###############################"


def draw_graph():

  X = []
  Y = []
  percent = 0.0
  for value in sorted(DIST):
    percent += DIST[value]

    X.append(value)
    Y.append(percent)
  
  
  line=(plt.plot(range(1, len(X)+1),Y))
  plt.setp(line,color='b', linewidth=4,ls='-')

  ax.set_ylim(0.1, 1)
  ax.set_xlim(1, 100)
  plt.xlabel("SLOC",fontsize=20)
  plt.ylabel("CDF",fontsize=20)
  
  currentAxis = plt.gca()

  currentAxis.add_patch(Rectangle((21 , 0), 0, 0.7, fill=False, color = 'g', linewidth = 4, ls = "-."))
  currentAxis.add_patch(Rectangle((0 , 0.7), 21, 0,   fill=False, color = 'g', linewidth = 4, ls = "-."))
  

  currentAxis.add_patch(Rectangle((32 , 0), 0, 0.8, fill=False, color = 'y', linewidth = 4, ls = "-."))
  currentAxis.add_patch(Rectangle((0 , 0.8), 32, 0,   fill=False, color = 'y', linewidth = 4, ls = "-."))

  currentAxis.add_patch(Rectangle((58 , 0), 0, 0.9, fill=False, color = 'red', linewidth = 4, ls = "-."))
  currentAxis.add_patch(Rectangle((0 , 0.9), 58, 0,   fill=False, color = 'red', linewidth = 4, ls = "-."))

#  plt.legend(("Broke rule","Followed Rule"),loc=0,fontsize=20)

  for label in ax.get_xticklabels():
    label.set_fontsize(18)
  for label in ax.get_yticklabels():
    label.set_fontsize(18)
  plt.grid(True)
  plt.tight_layout() 
  plt.show()

if __name__ == "__main__":
  
  global feature_to_look
  global intro_or_end
  global discardSmall
  
  feature_to_look = "SLOCStandard"
  intro_or_end = 1 ### 0 means intro
  discardSmall = 0 
      
  list_projects()
  find_indexes(feature_to_look)
  calculate_thresholds()
  #if feature_to_look == "McCabe":
  draw_graph()
  
