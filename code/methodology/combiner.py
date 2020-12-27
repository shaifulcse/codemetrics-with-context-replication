import re
import os
import matplotlib.pyplot as plt
#import numpy as np
#from  scipy import stats
from matplotlib.patches import Rectangle

fig = plt.figure()
ax = fig.add_subplot(111)

styles=["-", "--","-.", ":", "-", "--","-.", ":"]
marks=["^", "d", "o", "v", "p", "s", "<", ">"]
width = [3,3,3]
marks_size=[0, 0, 5, 15, 17, 10, 12,15]
marker_color=['#0F52BA','#ff7518','#6CA939','#e34234','#756bb1','brown','#c994c7', '#636363']



def draw_graph(lines):
  index = 0
  for line in lines:

    if len(line)<5:
      break

    line = line.strip()

    data = line.split('\t')
    
    y = []
    for i in range(1, len(data)):
      y.append(float(data[i]))
    #ln=plt.plot(range(0, len(y)),y)
    #plt.setp(ln,color='b', linewidth=4,ls='-')
    ln=(plt.plot(range(0, len(y)),y))
    plt.setp(ln,linewidth=width[index],ls=styles[index], marker = marks[index] ,markersize = marks_size[index], color=marker_color[index])
    index += 1
  currentAxis = plt.gca()
  currentAxis.add_patch(Rectangle((730 , 0.0), 0, 0.9, fill=False, color = 'red', linewidth = 3))
  
  plt.legend((['Age','All changes', 'Subsequent changes']),loc=0,fontsize=16)
  plt.xlabel("Day",fontsize=20)
  plt.ylabel("CDF",fontsize=20)  
  plt.xscale("log")
  for label in ax.get_xticklabels():
    label.set_fontsize(20)
  for label in ax.get_yticklabels():
    label.set_fontsize(20)
  plt.grid(True)  
  plt.tight_layout() 
  plt.show()

def read_data():
  fr = open("combined-data.csv",'r')
  lines = fr.readlines()
  fr.close()
  draw_graph(lines)

if __name__ == "__main__":
  read_data()      
 
