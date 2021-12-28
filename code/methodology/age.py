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
  age_2 = 0
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
      if age > 730:
        age_2 += 1
      c+=1
      if age not in AGES:
        AGES[age] = 1
      else:
        AGES[age] += 1 
    print project, c    
    tot+=c
  print tot, age_2    
def draw_graph(cdf):

  line=(plt.plot(range(0, len(cdf)),cdf))
  plt.setp(line,color='b', linewidth=4,ls='-')

  #ax.set_ylim(0, 1)
  #ax.set_xlim(1, 12)
  plt.xlabel("Age (days)",fontsize=20)
  plt.ylabel("CDF",fontsize=20)

#  plt.legend(("Broke rule","Followed Rule"),loc=0,fontsize=20)

  plt.xscale("log")

  for label in ax.get_xticklabels():
    label.set_fontsize(18)
  for label in ax.get_yticklabels():
    label.set_fontsize(18)

  currentAxis = plt.gca()

  currentAxis.add_patch(Rectangle((365 , 0), 0, 0.0886736745749, fill=False, color = 'r', linewidth = 4, ls = "-."))
  currentAxis.add_patch(Rectangle((0 , 0.0886736745749), 365, 0, fill=False, color = 'r', linewidth = 4, ls = "-."))

  currentAxis.add_patch(Rectangle((730 , 0), 0, 0.184432164348, fill=False, color = 'r', linewidth = 4, ls = "-."))
  currentAxis.add_patch(Rectangle((0 , 0.184432164348), 730, 0, fill=False, color = 'r', linewidth = 4, ls = "-."))
  plt.grid(True)
  plt.show()

def find_max():
  global MAX
  for age in AGES:
    
    if MAX<int(age):
      MAX = int(age)

def build_cdf():

  total = 0.0
  for age in AGES:
    total += AGES[age]

  find_max()
  cdf = [0.0]*(MAX+1)
  prev = 0.0

  for age in range(MAX+1):

    if age not in AGES:
      prob = 0.0
    else:
      prob = AGES[age]/total

    cdf[age] += prob + prev
    prev =  cdf[age]
 
  return cdf
  
def write(cdf):
  fw = open("combined-data.csv","w")
  fw.write("age\t")
  for i in range(len(cdf)):
    fw.write(str(cdf[i])+"\t")
  fw.write("\n")
  fw.close()

if __name__ == "__main__":
      
  list_projects()
  index = find_index("Age", "checkstyle")
  parse_age(index)
  cdf = build_cdf()
 
  draw_graph(cdf)
  write(cdf)
 
