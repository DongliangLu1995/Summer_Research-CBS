# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 20:00:16 2018

@author: DongliangLu
"""

#crawler cftc meeting about doddfrank
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def find_date(date_inf):
    date=date_inf.text
    date_pattern=re.compile(r"\d+/\d+/\d+")
    if date_pattern.findall(date):
        return date_pattern.findall(date)[0]
    else:
        return "default"
    
def find_org(org_inf):
    org=org_inf.text
    org_pattern=re.compile(r"[^\n\t]+")
    if org_pattern.findall(org):
        #len(...) always =1
        #return org_pattern.findall(org)[0]
        pattern=re.compile(r'\t.+\n')
        return pattern.findall(str(org_inf))[0].replace("\n","").replace("\t","").replace("<br/><br/>","||")
    else:
        return "default"    
    
def find_topic(topic_inf):
    topic=topic_inf.text
    topic_pattern=re.compile(r"[^\n\t]+")
    if topic_pattern.findall(topic):
        #len(...) always=2
#        print(len(topic_pattern.findall(topic)))
#        return "||".join(topic_pattern.findall(topic))
#        if len(topic_pattern.findall(topic))!=2:
#            print(len(topic_pattern.findall(topic)))
        pattern=re.compile(r'\t.+\n')
        
        return pattern.findall(str(topic_inf))[0].replace("\n","").replace("\t","").replace("<br/><br/>","||").replace("<br/>","")
    else:
        return "default" 

url="http://www.cftc.gov/LawRegulation/DoddFrankAct/ExternalMeetings/ExternalMeetingsAll/index.htm"
basic_url="www.cftc.gov"
soup = BeautifulSoup(requests.get(url).text,"lxml")



meetings=soup.find_all("div",class_="row")
meeting_data=[]
for meeting in meetings:
    meeting_data.append({})
    date_inf=meeting.find_all("div", class_="column-date")[0]
    meeting_data[-1]["date"]=find_date(date_inf)
    meeting_data[-1]["url"]=basic_url+date_inf.a['href']
    org_inf=meeting.find_all("div", class_="column-coltwo")[0]
    meeting_data[-1]["organization"]=find_org(org_inf)
    topic_inf=meeting.find_all("div", class_="column-colthree")[0]
    meeting_data[-1]["topic"]=find_topic(topic_inf)

df=pd.DataFrame(meeting_data)
df.to_csv("D:\\chromedownload\\Meeting_CFTC.csv")


    












