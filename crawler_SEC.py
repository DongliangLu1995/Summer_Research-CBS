# -*- coding: utf-8 -*-
"""
Created on Tue May 15 13:06:36 2018

@author: DongliangLu
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import pickle

#Href=get_comments_hrf(comments_SEC_herf,basic_url)
#def get_comments_hrf(L,basic_url):
#    H=[]
#    for i in range(1,len(L)):
#        if L[i].a:
#            H.append(basic_url+L[i].a["href"])
#    return H
        
def get_small_rule_name(L_i):
    return L_i.split("\n")[0]

#url="https://www.sec.gov/comments/s7-41-11/s74111.shtml#meetings"
url=r"https://www.sec.gov/spotlight/regreformcomments.shtml"
basic_url=r"https://www.sec.gov"
soup = BeautifulSoup(requests.get(url).text,"lxml")

#comments_SEC_herf=soup.find_all("i")
#len(comments_SEC_herf)=75
#drop the 0, and other has not a .a


tem=soup.find_all("li")
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
#def get_comments_hrf(L,basic_url):
#    H=[]
#    Rule_type=[]
#    for i in range(len(L)-36):
#        if L[i].b:
#            Rule_type.append(L[i].b.text)
#            H.append({})
#            key_cur=L[i].b.text
#        else:
#            small_rule_name=L[i].contents[0]
#            small_rule_url_list=L[i].find_all("i")
#            for ii in small_rule_url_list:
#                if ii.a:
#                    small_url=basic_url+ii.a["href"]
#                
#            H[-1][small_rule_name]=small_url
#
#    return H

Href=get_comments_hrf(tem,basic_url)


#add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"
#pickle.dump(Href,open(add+'\\'+"SEC_Href"+".pickle","wb"))
#with open(add+'\\'+"SEC_Href"+".pickle",'rb') as f:
#            Href=pickle.load(f, encoding='latin1')




for key1 in Href.keys():
    print()
    print(key1)
    for key2 in Href[key1].keys():
        print(key2)
        print(Href[key1][key2])

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







df_SEC_h=pd.DataFrame(Href["Other"])







#meetings=soup.find_all("tr",onmouseover="this.bgcolor='#E0E0E0'")
#meeting_start=find_meeting_index(meetings)
#
#SEC_v=[]
#for i in range(meeting_start, len(meetings)):
#    meeting_inf=meetings[i].a.text
#    pdf_url=basic_url+meetings[i].a["href"]
#    dates=grab_date(meeting_inf)
##    if not dates:
##        print(meeting_inf)
#    for date in dates:
#        SEC_v.append({})
#        SEC_v[-1]["date"]=date
#        org=grab_org(meeting_inf)
#        org=org_strip(org)
#        SEC_v[-1]["organization"]=org
#        SEC_v[-1]["url"]=pdf_url
























