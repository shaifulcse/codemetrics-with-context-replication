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
DIST ={}
feature_to_look = "Age"
AGES={}
MAX = 0

def list_projects():
  fr = open(PROJECTS_LIST,"r")
  lines = fr.readlines()
  fr.close()
  projects = []
  c = 0
  for line in lines:
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

def parse_age(index):
  tot = 0
  old = 0
  for project in PROJECTS:
    c = 0  
    fr = open(RESULT_PATH+project+".txt")
    line =  fr.readline() ## header
    lines = fr.readlines()
    fr.close()
    
    for line in lines:
      line = line.strip()
      data = re.findall("[^\t]+",line)
      age = int(data[index])
      c+=1
      if age>=730:
        old += 1
      if age not in AGES:
        AGES[age] = 1
      else:
        AGES[age] += 1 

    tot+=c
    DIST[project] = c

  ls =  sorted(DIST.items(), key=lambda x: x[1], reverse = True)
 
  for item in ls:
    print item

  print tot, old 

if __name__ == "__main__":
      
  list_projects()
  index = find_index("Age", "checkstyle")
  parse_age(index)
 
