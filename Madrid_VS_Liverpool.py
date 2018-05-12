# -*- coding: utf-8 -*-
"""
Created on Sat May 12 10:15:21 2018

@author: Karim Noor Ali
"""

from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np
from urllib.request import urlopen as uReq

#**********************************Extracting Liverpool Stats******************************************
url = 'http://www.uefa.com/uefachampionsleague/season=2018/clubs/club=7889/statistics/index.html'
uClient = uReq(url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html,"html.parser")
L_Stats = page_soup.findAll("div",{"class":"stats--aggregated grid_4"})

labels2 = L_Stats[1].findAll("span",{"class":"statistics--list--label"})
label2_stats= L_Stats[1].findAll("div",{"class":"statistics--list--data"})

Performance_Label = []
Performance_Stats = []
j = 0
for label in labels2:
    Performance = label.text
    Performance_Label.append(Performance)
    Stats = label2_stats[j].text
    Performance_Stats.append(Stats)
    j+=1

labels = L_Stats[2].findAll("span",{"class":"statistics--list--label"})
label_stats= L_Stats[2].findAll("div",{"class":"statistics--list--data"})


#*********************************Extracting labels and stats from the html******************************
i=0
for label in labels:
    Performance = label.text
    Performance_Label.append(Performance)
    Stats = label_stats[i].text
    if("\n" not in Stats):
        Performance_Stats.append(Stats)
    else:
        Stats = Stats.replace("\n","")
        Performance_Stats.append(Stats)       
    i+=1
  
Performance_Label[4] = "Passing Accuracy"
Performance_Label.pop(5)
Performance_Stats.pop(5)

#****************************Cleaning Data******************************************************

k = 0
for stats in Performance_Stats:
    if("%" in stats):
        stats = stats.replace("%","")
        Performance_Stats[k] = stats
    elif("km" in stats):
        stats, garbage1= stats.split(" ")
        Performance_Stats[k] = stats
    else:
        Performance_Stats[k] = stats
    k+=1

#***********************************Extracting Liverpool Defending Stats********************************************
L_Stats3 = page_soup.findAll("div",{"class":"stats--aggregated grid_2"})
Def_Label = L_Stats3[1].findAll("span",{"class":"statistics--list--label"})
Def_Stat = L_Stats3[1].findAll("div",{"class":"statistics--list--data"})


d=0
for label in Def_Label:
    Attr = label.text
    Performance_Label.append(Attr)
    Stats = Def_Stat[d].text
    Performance_Stats.append(Stats)
    d+=1

#***********************************Extracting Liverpool Attacking Stats********************************************
L_Stats4 = page_soup.findAll("div",{"class":"stats--aggregated grid_6"})
Att_Label = L_Stats4[0].findAll("span",{"class":"statistics--list--label"})
Att_Stat = L_Stats4[0].findAll("div",{"class":"statistics--list--data"})
Performance_Stats.append(Att_Stat[0].text) #Total goals scored
Performance_Stats.append(Att_Stat[2].text) #Total attempts
Performance_Label.append(Att_Label[0].text) #Total goals scored label
Performance_Label.append(Att_Label[2].text) #Total attempts label

#*********************************Converting data types in order visualise it****************************   
Performance_Stats = list(map(float, Performance_Stats))    
    
#**********************************Extracting Real Madrid Stats******************************************
#*******************Copying all of the above code, Just changing variables name**************************
M_url = 'https://www.uefa.com/uefachampionsleague/season=2018/clubs/club=50051/statistics/index.html'
uClient_M = uReq(M_url)
M_page_html = uClient_M.read()
uClient_M.close()

M_page_soup = soup(M_page_html,"html.parser")
M_Stats = M_page_soup.findAll("div",{"class":"stats--aggregated grid_4"})

Mlabels2 = M_Stats[0].findAll("span",{"class":"statistics--list--label"})
Mlabel2_stats= M_Stats[0].findAll("div",{"class":"statistics--list--data"})


M_Performance_Label = []
M_Performance_Stats = []
j = 0
for label in Mlabels2:
    M_Performance = label.text
    M_Performance_Label.append(M_Performance)
    Stats = Mlabel2_stats[j].text
    M_Performance_Stats.append(Stats)
    j+=1

Mlabels = M_Stats[1].findAll("span",{"class":"statistics--list--label"})
Mlabel_stats= M_Stats[1].findAll("div",{"class":"statistics--list--data"})

i=0
for label in Mlabels:
    M_Performance = label.text
    M_Performance_Label.append(M_Performance)
    Stats = Mlabel_stats[i].text
    if("\n" not in Stats):
        M_Performance_Stats.append(Stats)
    else:
        Stats = Stats.replace("\n","")
        M_Performance_Stats.append(Stats)       
    i+=1

M_Performance_Label[4] = "Passing Accuracy"
M_Performance_Label.pop(5)
M_Performance_Stats.pop(5)

k = 0
for stats in M_Performance_Stats:
    if("%" in stats):
        stats = stats.replace("%","")
        M_Performance_Stats[k] = stats
    elif("km" in stats):
        stats, garbage1= stats.split(" ")
        M_Performance_Stats[k] = stats
    else:
        M_Performance_Stats[k] = stats
    k+=1

#***********************************Extracting Real Madrids Defending Stats********************************************
M_Stats3 = M_page_soup.findAll("div",{"class":"stats--aggregated grid_2"})
MDef_Label = M_Stats3[0].findAll("span",{"class":"statistics--list--label"})
MDef_Stat = M_Stats3[0].findAll("div",{"class":"statistics--list--data"})


d=0
for label in MDef_Label:
    Attr = label.text
    M_Performance_Label.append(Attr)
    Stats = MDef_Stat[d].text
    M_Performance_Stats.append(Stats)
    d+=1
    

#***********************************Extracting Real Madrid Attacking Stats********************************************
M_Stats4 = M_page_soup.findAll("div",{"class":"stats--aggregated grid_6"})
MAtt_Label = M_Stats4[0].findAll("span",{"class":"statistics--list--label"})
MAtt_Stat = M_Stats4[0].findAll("div",{"class":"statistics--list--data"})
M_Performance_Stats.append(MAtt_Stat[0].text) #Total goals scored
M_Performance_Stats.append(MAtt_Stat[2].text) #Total attempts

#*********************************Converting data types in order visualise it**************************** 
M_Performance_Stats = list(map(float, M_Performance_Stats))    

#**********************Converting into data frame***************************************************
df = pd.DataFrame({"Label":Performance_Label,"Liverpool Stats":Performance_Stats,"Real Madrid Stats":M_Performance_Stats})

#************************Saving the file in Excel***************************************************
df.to_excel('D:\Data Science Journey/RM vs LIV Stats.xlsx',columns=['Label','Liverpool Stats','Real Madrid Stats'],index=False)




