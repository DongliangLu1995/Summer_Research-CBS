# -*- coding: utf-8 -*-
"""
Created on Thu May 17 17:24:39 2018

@author: DongliangLu
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import pickle


#add1=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\backup"
#add1+="\\SEC_comments_old.csv"
#SEC_comments_data=pd.read_csv(add1,index_col=0)
#rule_type_dic={}
#rule_type_list=SEC_comments_data["rule type"].unique()
#for i in range(len(rule_type_list)):
#    rule=rule_type_list[i]
#    rule_type_dic[rule]=i
#pickle.dump(rule_type_dic,open(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\backup"+"\\rule_type_dic.pickle","wb"))

with open(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\backup"+"\\rule_type_dic.pickle","rb") as f:
    tem=pickle.load(f, encoding='latin1')
rule_type_dic=tem


def find_memo(meeting):
    return "Memorandum" in meeting.text
        

def find_meeting_index(meetings):#only work for this network
    l=len(meetings)
    i=0
    j=l-1
    while i<j:
        m=int((i+j)/2)
        if find_memo(meetings[m]):
            if not find_memo(meetings[m-1]):
                return m
            else:
                j=m-1
        else:
            i=m+1
            if i>=l-1:
                return l#if not have any meetings, return none
    return i

def grab_org(meeting_inf):
    start=meeting_inf.find("call with")
    if start!=-1:
        meeting_inf=meeting_inf[start+10:]
    elif meeting_inf.find("calls with")!=-1:
        start=meeting_inf.find("calls with")
        meeting_inf=meeting_inf[start+11:]
    else:
        start=meeting_inf.find("meeting with")
        meeting_inf=meeting_inf[start+13:]
    return meeting_inf

def org_strip(org):
    org=org.replace("Counsel for ", "")
    org=org.replace("a representative of ","")
    org=org.replace("representatives of ","")
    org=org.replace("representatives from ","")
    return org

def grab_date(meeting_inf):
    month=["January","February","March","April","May","June","July","August",
           "September","October","November","December"]
    month="|".join(month)
    pattern=re.compile("("+month+")"+r"[\ ,]*(\d+)[\ ,]*(\d+)")
    dates= [", ".join(date) for date in pattern.findall(meeting_inf)]
    if not dates:
        dates=["April, 10, 2012 "]
    return dates        

def grab_date_c(comment_inf):
    date="".join(comment_inf.split()[0:3])
    return date

#url="https://www.sec.gov/comments/s7-41-11/s74111.shtml#meetings"
url=r"https://www.sec.gov/spotlight/regreformcomments.shtml"
basic_url=r"https://www.sec.gov"
soup = BeautifulSoup(requests.get(url).text,"lxml")

#comments_SEC_herf=soup.find_all("i")
#len(comments_SEC_herf)=75
#drop the 0, and other has not a .a


SEC_herf=soup.find_all("li")
#len(tem)=46
#{ "type1": {1:xxx,2:xxx } }
#xxx is the url
def get_comments_hrf(L,basic_url):
    H={}
    for i in range(len(L)):
        if L[i].b:
            H[L[i].b.text]={}
            key_cur=L[i].b.text
        else:
            small_rule_name=L[i].contents[0]
            small_rule_url_list=L[i].find_all("i")
            for ii in small_rule_url_list:
                if ii.a:
                    small_url=basic_url+ii.a["href"]
                
            H[key_cur][small_rule_name]=small_url

    return H

Href=get_comments_hrf(SEC_herf,basic_url)

k1="Title II — Orderly Liquidation Authority"
k2="Orderly Liquidation of Covered Broker-Dealers"
#Href[k1][k2]
Href[k1][1]="https://www.sec.gov/comments/s7-41-11/s74111.shtml"
Href[k1][2]="https://www.sec.gov/comments/df-title-vii/swap/swap.shtml"
#Href[k1][3]="https://www.sec.gov/comments/df-title-vii/swap/swap.shtml"
#k1="Title VI — Improvements to Regulation of Bank and Savings Associations Holding Companies and Depository Institutions"
#Href[k1][1]="https://www.sec.gov/comments/s7-41-11/s74111.shtml"
#k2='Title IV — Regulation of Advisers to Hedge Funds and Others'
#Href[k2][2]=
#"https://www.sec.gov/comments/s7-37-10/s73710.shtml"
#https://www.sec.gov/comments/s7-41-11/s74111.shtml
#https://www.sec.gov/comments/df-title-vii/swap/swap.shtml        
#https://www.sec.gov/comments/df-title-vii/swap/swap.shtml


#meeting_list=[]
#for key1 in Href.keys():
#    print()
#    print(key1)
#    for key2 in Href[key1].keys():
#        print(key2)
#        print(Href[key1][key2])
#        url_cur=Href[key1][key2]
#        soup_2=BeautifulSoup(requests.get(url_cur).text,"lxml")
#        title2=soup_2.find_all("h1")[0].text
#        
#        meetings=soup_2.find_all("tr",onmouseover="this.bgcolor='#E0E0E0'")
#        meeting_start=find_meeting_index(meetings)
#        
#        meeting_list_small=[]
#        for i in range(meeting_start, len(meetings)):
#            meeting_inf=meetings[i].a.text
#            pdf_url=basic_url+meetings[i].a["href"]
#            dates=grab_date(meeting_inf)
#        #    if not dates:
#        #        print(meeting_inf)
#            for date in dates:
#                meeting_list_small.append({})
#                meeting_list_small[-1]["date"]=date
#                org=grab_org(meeting_inf)
#                org=org_strip(org)
#                meeting_list_small[-1]["organization"]=org
#                meeting_list_small[-1]["url"]=pdf_url
#                meeting_list_small[-1]["rule type"]=title2
#                
#        meeting_list.append(meeting_list_small)

meeting_list=[]
for key1 in Href.keys():
    print()
    print(key1)
    for key2 in Href[key1].keys():
        print(key2)
        print(Href[key1][key2])
        url_cur=Href[key1][key2]
        soup_2=BeautifulSoup(requests.get(url_cur).text,"lxml")
        title2=soup_2.find_all("h1")[0].text
        
        meetings=soup_2.find_all("tr",onmouseover="this.bgcolor='#E0E0E0'")
        meeting_start=find_meeting_index(meetings)
        

        for i in range(meeting_start, len(meetings)):
            meeting_inf=meetings[i].a.text
            pdf_url=basic_url+meetings[i].a["href"]
            dates=grab_date(meeting_inf)
        #    if not dates:
        #        print(meeting_inf)
            for date in dates:
                meeting_list.append({})
                meeting_list[-1]["date"]=date
                org=grab_org(meeting_inf)
                org=org_strip(org)
                meeting_list[-1]["organization"]=org
                meeting_list[-1]["url"]=pdf_url
                meeting_list[-1]["rule type"]=title2
                
        



        
df_SEC_meeting=pd.DataFrame(meeting_list)
df_SEC_meeting.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"+r"\SEC_meetings.csv")
        
        
        


#grab cpmments
comment_list=[]
for key1 in Href.keys():
    print()
    print(key1)
    for key2 in Href[key1].keys():
        print(key2)
        print(Href[key1][key2])
        url_cur=Href[key1][key2]
        soup_2=BeautifulSoup(requests.get(url_cur).text,"lxml")
        title2=soup_2.find_all("h1")[0].text
        
        comments=soup_2.find_all("tr",onmouseover="this.bgcolor='#E0E0E0'")
        meeting_start=find_meeting_index(comments)
        

        for i in range(0, meeting_start):
            comment_content=comments[i].text
            date=grab_date_c(comment_content)
            people=" ".join(comment_content.split()[3:])
            comment_url=basic_url+comments[i].a["href"]
        #    if not dates:
        #        print(meeting_inf)

            comment_list.append({})
            comment_list[-1]["date"]=date
            comment_list[-1]["people"]=people
            comment_list[-1]["url"]=comment_url
            comment_list[-1]["rule type"]=title2

df_SEC_comment=pd.DataFrame(comment_list)
df_SEC_comment.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"+r"\SEC_comments.csv")


#key1[0]="Title II — Orderly Liquidation Authority"
#key2[0]="Orderly Liquidation of Covered Broker-Dealers"
k1="Title II — Orderly Liquidation Authority"
k2="Orderly Liquidation of Covered Broker-Dealers"
Href[k1][k2]
#'https://www.sec.gov/comments/df-title-ii/bd-liquidation/bd-liquidation.shtml'


soup_2=BeautifulSoup(requests.get(Href[k1][k2]).text,"lxml")
title2=soup_2.find_all("h1")[0].text
#'Orderly Liquidation of Covered Broker-Dealers: 
    #\r\nTitle II Provisions of the Dodd-Frank Wall Street Reform and Consumer Protection Act'

#len(soup_2.find_all("p"))


com_i=soup_2.find_all("tr",onmouseover="this.bgcolor='#E0E0E0'")

soup_2.find_all("tr",rowspan="2",width="10")