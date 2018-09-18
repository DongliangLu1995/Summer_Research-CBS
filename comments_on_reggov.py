# -*- coding: utf-8 -*-
"""
Created on Thu May 17 10:06:39 2018

@author: DongliangLu
"""

#regulation.gov
#find comments for different agencies

#FSOC
#https://www.regulations.gov/searchResults?rpp=300&po=0&s=Dodd%2BFrank&fp=true&dct=FR%2BPR%2BN%2BO&a=FSOC

#Treasury
#https://www.regulations.gov/searchResults?rpp=300&po=0&s=Dodd%2BFrank&fp=true&dct=FR%2BPR%2BN%2BO&a=FSOC%2BTREAS
#actually covered in FSOC
#Advance Notice of Proposed Rulemaking Regarding Authority To Require Supervision and Regulation of Certain Nonbank Financial Companies  
#for this example, the same


#FDIC
#https://www.regulations.gov/searchResults?rpp=300&po=0&s=Dodd%2BFrank&fp=true&dct=FR%2BPR%2BN%2BO&a=FDIC
#actually none

#FRS
#https://www.regulations.gov/searchResults?rpp=1000&po=0&s=Dodd%2BFrank&fp=true&dct=FR%2BPR%2BN%2BO&a=FRS
#actually none

#OCC

#CFTC
#https://www.regulations.gov/searchResults?rpp=300&po=300&s=Dodd%2BFrank&fp=true&dct=FR%2BPR%2BN%2BO&a=CFTC
#no comments

#CFPB
#https://www.regulations.gov/searchResults?rpp=3600&po=0&s=Dodd%2BFrank&dct=FR%2BPR%2BN%2BO&a=CFPB






#so we only need to do is FSOC



import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import math
import pandas
import requests
import pickle


def find_len(s):
    r='[a-zA-Z0-9]+'
    ws = re.findall(r,s)
    l=len(ws)
    return l

def redeal_filename(name):
    name=name.replace(".","_")
    name=name.replace("_&","")
    name=name.replace("__","_")
    return name    





#find which pages are having comments on them

driver = webdriver.Chrome()
basic_url="https://www.regulations.gov"
#url="https://www.regulations.gov/searchResults?rpp=300&po=0&s=Dodd%2BFrank&fp=true&dct=FR%2BPR%2BN%2BO&a=FSOC"
#url="https://www.regulations.gov/searchResults?rpp=300&po=0&s=Dodd%2BFrank&fp=true&dct=FR%2BPR%2BN%2BO&a=OCC"
url="https://www.regulations.gov/searchResults?rpp=3600&po=0&s=Dodd%2BFrank&dct=FR%2BPR%2BN%2BO&a=CFPB"
driver.get(url)
time.sleep(10)
html=driver.page_source
soup = BeautifulSoup(html, "lxml")


sub_webs=soup.find_all("li",class_="GIY1LSJNWC")
sub_web_url_list=[]
for sub_web in sub_webs:
    sub_url=basic_url+sub_web.find_all("a",class_="GIY1LSJEXC")[0]["href"]
    sub_web_url_list.append(sub_url)
driver.close()
save_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"+r"\CFPB_comments_web_mother.pickle"
pickle.dump(sub_web_url_list, open(save_add,"wb"))
with open(save_add,"rb") as f:
    tem=pickle.load(f, encoding='latin1')





comments_web=[]
#count=0
#128-128+85
for sub_web in sub_web_url_list[:]:
#    if count<=3:
    driver = webdriver.Chrome()
    driver.get(sub_web)
    time.sleep(5)
    html=driver.page_source
    soup2 = BeautifulSoup(html, "lxml")
    candidate_web=soup2.find_all("a",class_="GIY1LSJFWD")
    #use the one whose dct=ps 
    if candidate_web:
        for candidate in candidate_web:
            try:
                if "dct=PS" in candidate["href"]:
                    tem=basic_url+candidate["href"].replace("25","1500")
                    comments_web.append(tem)
            except:
                pass
    driver.close()
            
#    count+=1
comments_web=set(comments_web)
comments_web=list(comments_web)
save_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"+r"\CFPB_comments_web.pickle"
pickle.dump(comments_web, open(save_add,"wb"))
with open(save_add,"rb") as f:
    tem=pickle.load(f, encoding='latin1')

#comments_web[1] does not has a comment
#https://www.regulations.gov/docketBrowser?rpp=1500&so=DESC&sb=commentDueDate&po=0&dct=PS&D=FSOC-2011-0005
#
#temweb=comments_web[1]
#driver = webdriver.Chrome()
#driver.get(temweb)
#time.sleep(10)
#html=driver.page_source
#soup = BeautifulSoup(html, "lxml")
#soup.find_all("h3",class_="h2")[0].text.split()[0]=="0"
#soup.find_all("div",class_="GIY1LSJCID")

#agency="FSOC"
agency="CFPB"#has download pdf from 6-9
#for web_i in range(0,len(list(comments_web))):
for web_i in range(166,200):
    temweb=list(comments_web)[web_i]
    #this one has already been done and has really a lot of comments
    if temweb != 'https://www.regulations.gov/docketBrowser?rpp=1500&so=DESC&sb=commentDueDate&po=0&dct=PS&D=FSOC-2010-0002':
        url_comments=temweb
        
        comment=[]
        comment_pdf=[]
        name_same={}
        
        download_add="C:\\Users\\DongliangLu\\Desktop\\Columbia\\research\\CBS\\lobby\\comments_download\\"
        base_com_url="https://www.regulations.gov"
        Com_add=[]
        pdf_url=[]
        
        driver = webdriver.Chrome()
        driver.get(temweb)
        time.sleep(10)
        html=driver.page_source
        soup = BeautifulSoup(html, "lxml")
        #to see whether it has comments
        if soup.find_all("h3",class_="h2")[0].text.split()[0] != "0":
        
            rule_type=soup.find_all("div",class_="GIY1LSJCID")[0].text
            level1=soup.find_all("div",class_="GIY1LSJFYC GIY1LSJMXC")
            while not level1:
                time.sleep(5)
                html=driver.page_source
                soup = BeautifulSoup(html, "lxml")
                level1=soup.find_all("div",class_="GIY1LSJFYC GIY1LSJMXC")
            comments_download_add=download_add+agency+"\\add"+str(web_i)+".txt"
            with open(comments_download_add, 'w') as f:
                for com in level1:
                    try:
                        add_tag=com.find_all("div",class_="gwt-Hyperlink")
                        add=(add_tag[0].a)["href"]
                        com_add=base_com_url+add
                        Com_add.append(com_add)
                        f.write(com_add)
                        f.write("\n")
                    except:
                        pass
            print("writting address done")
            
            comment_crawler_now=1
            resume_num=0
            for i in range(resume_num,len(Com_add)):
                driver.get(Com_add[i])
                time.sleep(2)
                html2=driver.page_source
                soup2 = BeautifulSoup(html2, "lxml")
                sleep=0
                retry=0
                while (not sleep and retry<10):
                    level2=soup2.find_all("div",class_="GIY1LSJIXD")
                    if level2:
                        if level2[0].find_all("div",class_=""):
                            sleep=1
                        else:
                            time.sleep(2)
                            html2=driver.page_source
                            soup2 = BeautifulSoup(html2, "lxml")
                            retry+=1
                    else:
                        time.sleep(3)
                        html2=driver.page_source
                        soup2 = BeautifulSoup(html2, "lxml")
                        retry+=1
                print(i)
                if retry==10:
                    pass
                else:
                    #to see whether the comment is in pdf or not
                    pdf_or_not=soup2.find_all("div",class_="GIY1LSJA1D floatLeft")
                    if pdf_or_not:#has a pdf
                        comment_pdf.append({})
                        
                        pdf_name=soup2.find_all("h3",class_="GIY1LSJL1D")[0].text.replace(" ","_")
                        #pdf_name+=".pdf"
                        pdf_add=pdf_or_not[0].a["href"]
                        comment_pdf[-1]["pdf"]=1
                        comment_pdf[-1]["rule type"]=rule_type
                        comment_pdf[-1]["agency"]=agency
                        pdf_name=redeal_filename(pdf_name)
                        if pdf_name in name_same:
                            new_name=pdf_name+"("+str(name_same[pdf_name])+")"
                            name_same[pdf_name]+=1
                        else:
                            name_same[pdf_name]=1
                            new_name=pdf_name
                        comment_pdf[-1]["filename"]=new_name
                        
                        #other inf
                        level4=soup2.find_all("div",class_="GIY1LSJNTC")
                        date=level4[0].find_all("span",class_="breakWord",style="display: block;")[0].text
                        comment_pdf[-1]["date"]=date#submittion date
                        kind=level4[1].find_all("b",class_="breakWord")#the information kind
                        content=level4[1].find_all("span",class_="breakWord",style="display: block;")#inf
                        for i in range(len(kind)):
                            comment_pdf[-1][kind[i].text]=content[i].text
                        pdf_url.append(pdf_add)
                        
                    else:#don't has a pdf
                        comment.append({})
                        comment[-1]["pdf"]=0
                        comment[-1]["rule type"]=rule_type
                        comment[-1]["agency"]=agency
                        #comment
                        level2=soup2.find_all("div",class_="GIY1LSJIXD")
                        a=level2[0].find_all("div",class_="")
                        b=a[0].text#find the comment text
                        comment[-1]["comment"]=b#comment
                        comment[-1]["length"]=find_len(b)#length of comment
                        #other inf
                        level4=soup2.find_all("div",class_="GIY1LSJNTC")
                        date=level4[0].find_all("span",class_="breakWord",style="display: block;")[0].text
                        comment[-1]["date"]=date#submittion date
                        kind=level4[1].find_all("b",class_="breakWord")#the information kind
                        content=level4[1].find_all("span",class_="breakWord",style="display: block;")#inf
                        for i in range(len(kind)):
                            comment[-1][kind[i].text]=content[i].text
                comment_crawler_now+=1
            time.sleep(2)
            driver.close()
            comments_pdf_download_add=download_add+agency+"\\add_pdf_"+str(web_i)+".txt"
            with open(comments_pdf_download_add, 'w') as f2:
                for pdfurl in pdf_url:
                    f2.write(pdfurl)
                    f2.write("\n")
            print("writting PDF address done")
#    
#            driver = webdriver.Chrome()
#            for add in pdf_url:
#                time.sleep(2)
#                driver.get(add)
#            time.sleep(3)
#            driver.close()
        
            comment_total=comment+comment_pdf
            dataframe1=pandas.DataFrame(comment)
            dataframe2=pandas.DataFrame(comment_total)
            dataframepdf=pandas.DataFrame(comment_pdf)
            dataframe1.to_csv("C:\\Users\\DongliangLu\\Desktop\\Columbia\\research\\CBS\\lobby\\comments_download\\"+agency+"\\dataframe1_"+str(web_i)+".csv")
            dataframe2.to_csv("C:\\Users\\DongliangLu\\Desktop\\Columbia\\research\\CBS\\lobby\\comments_download\\"+agency+"\\dataframe2_"+str(web_i)+".csv")
            dataframepdf.to_csv("C:\\Users\\DongliangLu\\Desktop\\Columbia\\research\\CBS\\lobby\\comments_download\\"+agency+"\\dataframepdf_"+str(web_i)+".csv")
            #save_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"+r"\comments_web.pickle"
            pickle.dump(dataframe1, open("C:\\Users\\DongliangLu\\Desktop\\Columbia\\research\\CBS\\lobby\\comments_download\\"+agency+"\\dataframe1_"+str(web_i)+".pickle","wb"))
            pickle.dump(dataframe2, open("C:\\Users\\DongliangLu\\Desktop\\Columbia\\research\\CBS\\lobby\\comments_download\\"+agency+"\\dataframe2_"+str(web_i)+".pickle","wb"))
            pickle.dump(dataframepdf, open("C:\\Users\\DongliangLu\\Desktop\\Columbia\\research\\CBS\\lobby\\comments_download\\"+agency+"\\dataframepdf_"+str(web_i)+".pickle","wb"))
#with open(save_add,"rb") as f:
#    tem=pickle.load(f, encoding='latin1')
        else:
            driver.close()

























comment=[]
#comment=[ {pdf:0, comment:xx, comlength:xx, submitter:xx, date:xx, country:xx, city:xx, 
#             state:xx, organization:xx,xx:xx} ]
comment_pdf=[]
#comment=[ {pdf:1, pdf_add:xx, comment:xx, comlength:xx, submitter:xx, date:xx, country:xx, city:xx, 
#             state:xx, organization:xx,xx:xx} ]
name_same={}
    
base_com_url="https://www.regulations.gov"
download_add="D:\\chromedownload\\comment\\"

Com_add=[]
pdf_url=[]

page=0
driver = webdriver.Chrome()
url="https://www.regulations.gov/docketBrowser?rpp="+str(comment_per_page)+"&so=DESC&sb=commentDueDate&po="+str(page*comment_per_page)+"&dct=PS&D=FSOC-2010-0002"
driver.get(url)
time.sleep(20)
html=driver.page_source
soup = BeautifulSoup(html, "lxml")
level1=soup.find_all("div",class_="GIY1LSJFYC GIY1LSJMXC")
#from level1 we want to get the url of each comment
while not level1:
    time.sleep(5)
    html=driver.page_source
    soup = BeautifulSoup(html, "lxml")
    level1=soup.find_all("div",class_="GIY1LSJFYC GIY1LSJMXC")
with open('D:\\chromedownload\\add.txt', 'w') as f:
    for com in level1:
        add_tag=com.find_all("div",class_="gwt-Hyperlink")
        add=(add_tag[0].a)["href"]
        com_add=base_com_url+add
        Com_add.append(com_add)
        f.write(com_add)
        f.write("\n")
print("writting address done")


comment_crawler_now=1
resume_num=0
for i in range(resume_num,len(Com_add)):
    driver.get(Com_add[i])
    time.sleep(2)
    html2=driver.page_source
    soup2 = BeautifulSoup(html2, "lxml")
    sleep=0
    retry=0
    while (not sleep and retry<10):
        level2=soup2.find_all("div",class_="GIY1LSJIXD")
        if level2:
            if level2[0].find_all("div",class_=""):
                sleep=1
            else:
                time.sleep(2)
                html2=driver.page_source
                soup2 = BeautifulSoup(html2, "lxml")
                retry+=1
        else:
            time.sleep(3)
            html2=driver.page_source
            soup2 = BeautifulSoup(html2, "lxml")
            retry+=1
    print(i)
    if retry==10:
        pass
    else:
        #to see whether the comment is in pdf or not
        pdf_or_not=soup2.find_all("div",class_="GIY1LSJA1D floatLeft")
        if pdf_or_not:#has a pdf
            comment_pdf.append({})
            
            pdf_name=soup2.find_all("h3",class_="GIY1LSJL1D")[0].text.replace(" ","_")
            #pdf_name+=".pdf"
            pdf_add=pdf_or_not[0].a["href"]
            comment_pdf[-1]["pdf"]=1
            pdf_name=redeal_filename(pdf_name)
            if pdf_name in name_same:
                new_name=pdf_name+"("+str(name_same[pdf_name])+")"
                name_same[pdf_name]+=1
            else:
                name_same[pdf_name]=1
                new_name=pdf_name
            comment_pdf[-1]["filename"]=new_name
            
            #other inf
            level4=soup2.find_all("div",class_="GIY1LSJNTC")
            date=level4[0].find_all("span",class_="breakWord",style="display: block;")[0].text
            comment_pdf[-1]["date"]=date#submittion date
            kind=level4[1].find_all("b",class_="breakWord")#the information kind
            content=level4[1].find_all("span",class_="breakWord",style="display: block;")#inf
            for i in range(len(kind)):
                comment_pdf[-1][kind[i].text]=content[i].text
            pdf_url.append(pdf_add)
            
        else:#don't has a pdf
            comment.append({})
            comment[-1]["pdf"]=0
            #comment
            level2=soup2.find_all("div",class_="GIY1LSJIXD")
            a=level2[0].find_all("div",class_="")
            b=a[0].text#find the comment text
            comment[-1]["comment"]=b#comment
            comment[-1]["length"]=find_len(b)#length of comment
            #other inf
            level4=soup2.find_all("div",class_="GIY1LSJNTC")
            date=level4[0].find_all("span",class_="breakWord",style="display: block;")[0].text
            comment[-1]["date"]=date#submittion date
            kind=level4[1].find_all("b",class_="breakWord")#the information kind
            content=level4[1].find_all("span",class_="breakWord",style="display: block;")#inf
            for i in range(len(kind)):
                comment[-1][kind[i].text]=content[i].text
    comment_crawler_now+=1
time.sleep(3)
driver.close()
        
with open('D:\\chromedownload\\pdf_add.txt', 'w') as f2:
    for pdfurl in pdf_url:
        f2.write(pdfurl)
        f2.write("\n")
print("writting address done")


driver = webdriver.Chrome()
for add in pdf_url:
    time.sleep(2)
    driver.get(add)
time.sleep(3)
driver.close()
  
comment_total=comment+comment_pdf
dataframe1=pandas.DataFrame(comment)
dataframe2=pandas.DataFrame(comment_total)
dataframepdf=pandas.DataFrame(comment_pdf)
dataframe1.to_csv("D:\\chromedownload\\dataframe1.csv")
dataframe2.to_csv("D:\\chromedownload\\dataframe2.csv")
dataframepdf.to_csv("D:\\chromedownload\\dataframepdf.csv")






