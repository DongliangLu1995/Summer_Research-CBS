# -*- coding: utf-8 -*-
"""
Created on Sat May 26 08:50:01 2018

@author: DongliangLu
"""

#grab the comments of fed
#data source: https://www.federalreserve.gov/apps/foia/dfproposals.aspx


import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import math
import pandas
import requests
import pickle


driver = webdriver.Chrome()
basic_url="https://www.federalreserve.gov"
url="https://www.federalreserve.gov/apps/foia/dfproposals.aspx"
driver.get(url)
time.sleep(10)
html=driver.page_source
soup = BeautifulSoup(html, "lxml")


sub_webs=soup.find_all("li",class_="panel__listItem")
sub_web_url_list=[]
for sub_web in sub_webs:
    sub_web_item=sub_web.find_all("p")
    if len(sub_web_item)==4:
        try:
            sub_web_url_list.append({})
            sub_web_url_list[-1]["Agency Information Collection"]=sub_web_item[0].a.text
            sub_web_url_list[-1]["Agency Information URL"]=basic_url+sub_web_item[0].a["href"]
            sub_web_url_list[-1]["Content"]=sub_web_item[1].text
            sub_web_url_list[-1]["Closing Date"]=sub_web_item[2].text[-10:]
            sub_web_url_list[-1]["Comment Url"]=basic_url+"/apps/foia/"+sub_web_item[3].find_all("a")[1]["href"]
        except:
            pass
driver.close()
save_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"+r"\Fed_comments_web_mother.pickle"
pickle.dump(sub_web_url_list, open(save_add,"wb"))
with open(save_add,"rb") as f:
    tem=pickle.load(f, encoding='latin1')


basic_url="https://www.federalreserve.gov"
data_saveadd=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\comments_download\FED"
federal_mother = tem



for i in range(len(federal_mother)):
    print("solving rule "+str(i))
    Comment_url=federal_mother[i]['Comment Url'].replace("ViewComments","ViewALLComments")
    soup = BeautifulSoup(requests.get(Comment_url).text,"lxml")
    try:
        comments = soup.find_all("ul", class_="list-single-icon")[0].find_all("li")
        comment_sub=[]
        for comment in comments:
            comment_sub.append({})
            comment_pdf_url=basic_url+comment.a["href"]#if you want to download, you need to with open as ...
            comment_orginization=comment.a.text
            for key in federal_mother[i].keys():
                comment_sub[-1][key]=federal_mother[i][key]
            comment_sub[-1]["orginzation"]= comment_orginization  
            comment_sub[-1]["pdf url"]=comment_pdf_url
        rule_save_add=data_saveadd+"\\"+"Fed_comments_rule_"+str(i)+".pickle"
        rule_save_add_csv=data_saveadd+"\\"+"Fed_comments_rule_"+str(i)+".csv"
        pickle.dump(comment_sub, open(rule_save_add,"wb"))
        pandas.DataFrame(comment_sub).to_csv(rule_save_add_csv)
    except:
        pass
    




























