# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 10:00:59 2018

@author: DongliangLu
"""

#FDIC COMMENTS
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import pickle



comments_mother_FDIC=[]

#different for 2010-2011 and 2012-2017
#also the comments web sites are totally different for these two years
for year in range(2010,2012):
    url="https://www.fdic.gov/regulations/laws/federal/"+str(year)+"/index-"+str(year)+".html"
    basic_url_finding_comments="https://www.fdic.gov"
    soup = BeautifulSoup(requests.get(url).text,"lxml")
    comments_href=soup.find_all("tr")[1:]#0 is title

    for rule_i in range(len(comments_href)):
        if comments_href[rule_i].find_all("td")[-1].text.strip() =="Read Comments":
            comments_url=basic_url_finding_comments+comments_href[rule_i].find_all("td")[-1].a["href"]
            comments_mother_FDIC.append(comments_url)




for year in range(2012,2018):
    url="https://www.fdic.gov/regulations/laws/federal/"+str(year)+"/index-"+str(year)+".html"
    basic_url_finding_comments="https://www.fdic.gov/regulations/laws/federal/"
    soup = BeautifulSoup(requests.get(url).text,"lxml")
    comments_href=soup.find_all("tr")[1:]#0 is title

    for rule_i in range(len(comments_href)):
        if comments_href[rule_i].find_all("td")[-1].text.strip() =="Read Comments":
            comments_url=basic_url_finding_comments+str(year)+"/"+comments_href[rule_i].find_all("td")[-1].a["href"]
            comments_mother_FDIC.append(comments_url)

save_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"+r"\comments_mother_FDIC.pickle"
#pickle.dump(comments_mother_FDIC, open(save_add,"wb"))
with open(save_add,"rb") as f:
    tem=pickle.load(f, encoding='latin1')

#some of the urls may be incorrect
#use url[:51]+url[82:]
comments_mother_FDIC=tem
rule_saving_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\comments_download\FDIC"
comment_saving_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\comments_download\FDIC_PDF"
for rule_url_i in range(len(comments_mother_FDIC)):
#for rule_url_i in range(1):   
#sample problem rule:14,17,22,23,58,88-95
#rule_url_i=58
    url=comments_mother_FDIC[rule_url_i]
    soup = BeautifulSoup(requests.get(url).text,"lxml")
    try:
        pdf_basic_url="https://www.fdic.gov"
        a=soup.find_all("p")
        
        rule_summary=a[5].text
        rule_summary_save_add=rule_saving_add+r"\rule_summary_"+str(rule_url_i)+".txt"
        with open(rule_summary_save_add,"w") as f:
            f.write(rule_summary)
            
        pdf_url1=pdf_basic_url+a[6].a["href"]
        pdf_url2=url[:51]+a[6].a["href"]
        pdf_save_add=rule_saving_add+r"\related_rule_"+str(rule_url_i)+".pdf"
        try:
            r = requests.get(pdf_url1)
            with open(pdf_save_add,"wb") as f:
                f.write(r.content)
        except:
            r = requests.get(pdf_url2)
            with open(pdf_save_add,"wb") as f:
                f.write(r.content)

        comment_rule_i=[]
        b=soup.find_all("tr")[1:]
        for comment_i in range(len(b)):
            try:
                comment = b[comment_i]
                orginization = comment.text.strip().strip(" - PDF")
                rule_type =  rule_url_i
                comment_pdf_url = pdf_basic_url+comment.a["href"]
    #            try:
    #                comment_pdf_save_add = comment_saving_add+"\\rule_"+str(rule_url_i)+"_comment_"+ str(comment_i)+".pdf"
    #                r = requests.get(comment_pdf_url)
    #                with open(pdf_save_add,"wb") as f:
    #                    f.write(r.content)
    #            except:
    #                pass
                comment_rule_i.append({})
                comment_rule_i[-1]["rule number"]=rule_url_i
                comment_rule_i[-1]["orginization"]=orginization
                comment_rule_i[-1]["pdf_url"]=comment_pdf_url
            except:
                pass
        comment_rule_i_save_add=rule_saving_add+r"\comment_rule_"+str(rule_url_i)+".pickle"
        pickle.dump(comment_rule_i, open(comment_rule_i_save_add,"wb"))
        print(0)
    except:
        try:
#            rule_url_i=88
            try:
                url=comments_mother_FDIC[rule_url_i]
                soup = BeautifulSoup(requests.get(url).text,"lxml")
                a=soup.find_all("table",width="760")[0]
            except:
                url=comments_mother_FDIC[rule_url_i]
                url=url[:51]+url[82:]
                soup = BeautifulSoup(requests.get(url).text,"lxml")
    
            rule_summary=url[51:]
            rule_summary_save_add=rule_saving_add+r"\rule_summary_"+str(rule_url_i)+".txt"
            with open(rule_summary_save_add,"w") as f:
                f.write(rule_summary)
            
            a=soup.find_all("table",width="760")[0]
            try:
                pdf_url= url[:51]+a.td.find_all("a")[1]["href"]
                pdf_save_add=rule_saving_add+r"\related_rule_"+str(rule_url_i)+".pdf"
                r = requests.get(pdf_url)
                with open(pdf_save_add,"wb") as f:
                    f.write(r.content)
            except:
                pass
                
            comment_rule_i=[]
            for comment_i in range(len(a.tbody.find_all("tr"))):
                try:
                    comment=a.tbody.find_all("tr")[comment_i]
                    orginization = comment.text.strip().strip(" - PDF")
                    rule_type =  rule_url_i
                    comment_pdf_url = url[:51]+comment.a["href"]
        #            try:
        #                comment_pdf_save_add = comment_saving_add+"\\rule_"+str(rule_url_i)+"_comment_"+ str(comment_i)+".pdf"
        #                r = requests.get(comment_pdf_url)
        #                with open(pdf_save_add,"wb") as f:
        #                    f.write(r.content)
        #            except:
        #                pass
                    comment_rule_i.append({})
                    comment_rule_i[-1]["rule number"]=rule_url_i
                    comment_rule_i[-1]["orginization"]=orginization
                    comment_rule_i[-1]["pdf_url"]=comment_pdf_url
                except:
                    pass
            comment_rule_i_save_add=rule_saving_add+r"\comment_rule_"+str(rule_url_i)+".pickle"
            pickle.dump(comment_rule_i, open(comment_rule_i_save_add,"wb"))
        
                
            
            print(1)
        except:
            print("rule "+str(rule_url_i))
        
        
        

#with open(rule_summary_save_add, "r") as f:
#    tex=f.readlines()

#with open(comment_rule_i_save_add,"rb") as f:
#    tem=pickle.load(f, encoding='latin1')

















