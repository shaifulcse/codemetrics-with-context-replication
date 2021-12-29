import matplotlib.pyplot as plt
import re
import math

import seaborn as sns
import pandas as pd
sns.set(font_scale = 1.2)
fig = plt.figure()
ax = fig.add_subplot(111)


PROJECTS_LIST = "../../info/settings-project.txt"

RESULT_PATH="../../data/complexity-and-change-data/"
#RESULT_PATH="/home/shaiful/research/software-evolution/result/static-analysis/source-code/selected-features-corrected/"

PROJECTS = {}
STATS = {}

def list_projects():
  fr = open(PROJECTS_LIST,"r")
  lines = fr.readlines()
  fr.close()
  projects = []
  c = 0
  for line in lines:
  
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

    list_indexes(feature,project)    
    if project not in STATS:
      STATS[project] = {}
    if feature not in STATS[project]:
      STATS[project][feature] = {}
  
    fr = open(RESULT_PATH+project+".txt")
    line =  fr.readline() ## header
    lines = fr.readlines()
    fr.close()
    
    for line in lines:
        
      line = line.strip()      
      data = re.findall("[^\t]+",line)
      age = int(data[0])
       

      if apply_age_restriction == 1 and age <age_restriction:
        continue
      
      method = data[len(data)-1]

      STATS[project][feature][method]={}   
      STATS[project][feature][method]['Large']=[]
      STATS[project][feature][method]['All']=[]
   
      feature_values = re.findall("[^,]+",data[feature_index])
      sloc_values = re.findall("[^,]+",data[sloc_index])
      date_values = re.findall("[^,]+",data[date_index])
      diff_values = re.findall("[^,]+",data[diff_index])
      addition_values = re.findall("[^,]+",data[addition_index])
      edit_values = re.findall("[^,]+",data[edit_index])
     
      track = 0  
      for i in range(1, len(diff_values)):

        if int(date_values[i]) > age_restriction: ## change not within in time          
          break
        if int(diff_values[i]) == 0: ## no change in content      
          continue
        
        track = 1
        feature_value = float(feature_values[i-1]) 
        sloc = float(sloc_values[i-1])

        if sloc > 32:
          STATS[project][feature][method]['Large'].append(feature_value)
        STATS[project][feature][method]['All'].append(feature_value)
 
      if track == 0: ## there was no change
        feature_value = float(feature_values[0])         
        sloc = float(sloc_values[0])         
        if sloc > 32:
          STATS[project][feature][method]['Large'].append(feature_value)
        STATS[project][feature][method]['All'].append(feature_value) 



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


def write():
 
  fw = open("seaborn_data.csv","w")
  fw.write("project,method,Feature,Size,Value\n")
  for project in STATS:
    for feature in STATS[project]:
      for method in STATS[project][feature]:
     
        for size in STATS[project][feature][method]:          
          for value in  STATS[project][feature][method][size]:
            ft = feature
            if feature == 'Mcclure':
              ft = 'McClure';
            if feature == 'MaximumBlockDepth':
              ft = 'NBD'
            if feature == 'totalFanOut':
              ft = 'FanOut'

            if feature == 'MaintainabilityIndex':
              ft = 'MIndex'

            fw.write(project+","+method+","+ft+","+size+","+ str(value)+"\n")
            #print project+","+method+","+ft+","+size+","+ str(value)
  fw.flush()
  fw.close()

      
def graph():
  df = pd.read_csv('seaborn_data.csv')	
  #sns.boxplot(x="Feature", y="Value", hue="Size",  hue_order=['totalFanOut','Mcclure','McCabe', 'IndentSTD','MaximumBlockDepth', 'Readability'],   data=df, palette="Set2")
  b = sns.boxplot(x="Feature", y="Value", hue="Size", order = ['MIndex', 'FanOut','McClure','McCabe', 'IndentSTD','NBD', 'Readability'], hue_order=['All', 'Large'], data=df, palette="Set2")
  ax.set_ylim(-1, 160)

  #plt.yscale("log")
  plt.legend(loc=1,fontsize=18)
  for label in ax.get_xticklabels():
    label.set_fontsize(18)
  for label in ax.get_yticklabels():
    label.set_fontsize(17)
  b.set_ylabel("Value",fontsize=20)
  b.set_xlabel("Feature",fontsize=20)
  plt.tight_layout() 
  plt.xticks(rotation=25)
  plt.show()
      
if __name__ == "__main__":


  global feature 
  global age_restriction
  global all_features 
  apply_age_restriction = 1
  age_restriction = 730

    
  all_features =['McCabe','Mcclure','MaximumBlockDepth', 'IndentSTD','totalFanOut', 'Readability',  'MaintainabilityIndex']
  #all_features =['McCabe','Mcclure'] 
  legends = ['McCabe','McClure','NBD', 'IndentSTD','totalFanOut', 'Readability', 'MIndex']
  
  list_projects()
  
 ## enable these lines to run the whole program
  for feature in all_features:
    print feature  
    parse_data()
    
 
  write()
  print "drawing graph" 
    
  graph()
   
