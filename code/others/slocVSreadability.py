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
#RESULT_PATH="/home/shaiful/research/software-evolution/result/static-analysis/source-code/selected-features-corrected/"

SLOC = []
READABILITY = []
total = 0
exceeded = 0

def list_projects():
  fr = open(PROJECTS_LIST,"r")
  lines = fr.readlines()
  fr.close()
  projects = []
  c=0
  
  for line in lines:
   
    if len(line)<5:
      break 
    line = line.strip()
    data = re.findall("[^\t]+",line)
    projects.append(data[0])
  return projects


def find_index(feature, project):
  fr = open(RESULT_PATH+project+".txt")
  line =  fr.readline() ## header
  line = line.strip()
  data = re.findall("[^\t]+",line)
  for i in range(len(data)):
    if data[i] == feature:
      return i

def parse_data(projects, index_readability,index_sloc):
  global total
  global exceeded
  tot = 0
  for project in projects:
    fr = open(RESULT_PATH+project+".txt")
    line =  fr.readline() ## header
    lines = fr.readlines()
    fr.close()
    #print project
    c = 0
    for line in lines:
      line = line.strip()
      data = re.findall("[^\t]+",line)
      sloc = re.findall("[^,]+",data[index_sloc])
      sloc = int(sloc[0])
      total += 1
      if sloc>54:
        exceeded += 1
      c += 1
      SLOC.append(sloc)
      read = re.findall("[^,]+",data[index_readability])
      read = float(read[0])
      READABILITY.append(read) 
    print project, c
    tot += c
  print tot
def draw_graph():
  plt.scatter(SLOC, READABILITY, color ="#0F52BA")
  #ax.set_ylim(0, 1)
  ax.set_xlim(1, 100)
  plt.xlabel("SLOC", fontsize = 18)
  plt.ylabel("Readability",fontsize = 18)

 # ax.set_yscale('log')
 # ax.set_xscale('log')
#  plt.legend(("All","Successful"),loc=0,fontsize=20)

  for label in ax.get_xticklabels():
    label.set_fontsize(18)
  for label in ax.get_yticklabels():
    label.set_fontsize(16)
  plt.tight_layout()

#  plt.grid(True)
#  plt.title(PROJECT,fontsize=20)

  currentAxis = plt.gca()
  currentAxis.add_patch(Rectangle((1 , 0.0), 11, 1, fill=False, color = 'red', linewidth = 3))

  currentAxis.add_patch(Rectangle((33 , 0.0), 0, 1, fill=False, color = 'red', linewidth = 3))
  plt.show()

if __name__ == "__main__":

  index_readability = find_index("Readability","checkstyle")
  index_sloc = find_index("SLOCStandard","checkstyle")
  projects = list_projects()
  parse_data(projects, index_readability,index_sloc)
  #test()
  draw_graph()
  print "total projects", len(projects)
  print "total methods", total
  print "exceeded 54 lines", exceeded
#  for file in os.listdir(RESULT_PATH):
#    print file


