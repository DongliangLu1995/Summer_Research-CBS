# -*- coding: utf-8 -*-
"""
Created on Thu May 31 14:09:52 2018

@author: DongliangLu
"""

#download final rule from https://www.stlouisfed.org/federal-banking-regulations/#
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import Select
import time
import pickle


driver = webdriver.Chrome()
url="https://www.stlouisfed.org/federal-banking-regulations/#"
driver.get(url)
time.sleep(5)
driver.find_element_by_id("btnFinal").click()
time.sleep(5)
html=driver.page_source
soup = BeautifulSoup(html, "lxml")
Final_rule_odd=soup.find_all("tr",class_="odd")
Final_rule_even=soup.find_all("tr",class_="even")

basic_url="https://www.stlouisfed.org"
save_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\final rule\final_rule_banking_download"
Final_rule_click=driver.find_elements_by_class_name(" sorting_2")
Final_rule_data=[]
pdf_download=[]
problem_rule=[]
click_range=len(Final_rule_click)
#16 3.6 FRS
#i=16
for i in range(477,click_range):
    Final_rule_click=driver.find_elements_by_class_name(" sorting_2")
    time.sleep(2)
    final_rule=Final_rule_click[i]
    final_rule.click()
    time.sleep(2)
    print("going to final rule "+str(i))
    html=driver.page_source
    soup=BeautifulSoup(html, "lxml")
    #soup.find_all("div",id_="divSummary")
#    count_max=2
    count=0
#    while (not soup.find_all("p",class_="summaryText")) and count<=count_max:
    while (not soup.find_all("p",class_="summaryText")):
        print("waiting for user to click the website")
        print("rule "+str(i))
        if i%2==0:#odd
            print(Final_rule_odd[i//2].text[:45])
            time.sleep(3)
            html=driver.page_source
            soup=BeautifulSoup(html, "lxml")
#            count+=1
        else:
            print(Final_rule_even[i//2].text[:45])
            time.sleep(3)
            html=driver.page_source
            soup=BeautifulSoup(html, "lxml")
    try:
        rule_summary=soup.find_all("p",class_="summaryText")[0].text.strip()
        rule_type=soup.find_all("h3")[0].text.strip()
        rule_type_number=i
        
        if soup.find_all("a", class_="summaryPDFLink"):
    #        pdf_url=basic_url+soup.find_all("p", style="margin-left:10px;")[0].a["href"]
            pdf_url=basic_url+soup.find_all("a", class_="summaryPDFLink")[0]["href"]
            pdf_download.append(pdf_url)
            
            pdf_save_add=save_add+"\\"+"final_rule_banking_"+str(rule_type_number)+".pdf"
            
            r = requests.get(pdf_url)
            with open(pdf_save_add, 'wb') as f:
                f.write(r.content)
            print("saving pdf for rule "+str(i)+ " done")
            
            date=soup.find_all("p",class_="speechnote")[0].text
            date=date.strip()
            date=date.split("\n")
            published_date=date[0].split(":")[1]
            effective_date=date[1].split(":")[1]
            agency=soup.find_all("p", style="margin-left:10px;")[1].text.strip()
            reference_number=soup.find_all("p", style="margin-left:10px; margin-top:0px;")[0].text.strip()
            
            Final_rule_data.append({})
    #        Final_rule_data[-1]["rule type"]=rule_type
            Final_rule_data[-1]["rule type number"]=rule_type_number
            
            #Final_rule_data[-1]["rule summary"]=rule_summary
            rule_summary_save_add=save_add+"\\"+"final_rule_banking_rule_summary_"+str(rule_type_number)+".txt"
            with open(rule_summary_save_add, 'w',encoding='utf-8') as f:
                f.write(rule_summary)
            print("writing summary for rule "+str(i)+ " done")
            rule_type_save_add=save_add+"\\"+"final_rule_banking_rule_type_"+str(rule_type_number)+".txt"
            with open(rule_type_save_add, 'w',encoding='utf-8') as f:
                f.write(rule_type)
            print("writing rule type for rule "+str(i)+ " done")
    #        Final_rule_data[-1]["pdf url"]=pdf_url
            Final_rule_data[-1]["published date"]=published_date
            Final_rule_data[-1]["effective date"]=effective_date
            Final_rule_data[-1]["agency"]=agency
            Final_rule_data[-1]["reference number"]=reference_number
        
        return_click=driver.find_elements_by_class_name("likeabutton")[0]
        return_click.click()
        time.sleep(2)
    except:
        print("not successfully download rule "+str(i))
        problem_rule.append(i)
    
pickle_save_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"+r"\final_rule_banking.pickle"
pickle.dump(Final_rule_data, open(pickle_save_add,"wb"))
pdf_pickle_save_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"+r"\final_rule_banking_pdf.pickle"
pickle.dump(pdf_download, open(pdf_pickle_save_add,"wb"))

with open(pickle_save_add,"rb") as f:
    tem=pickle.load(f, encoding='latin1')
with open(pdf_pickle_save_add,"rb") as f:
    tem=pickle.load(f, encoding='latin1')    
#with open(rule_summary_save_add,"r") as f:
#    a=f.readline()
    
    















#soup.find_all("div")
#
#tem=soup.find_all("ul",class_="brgNavBar")[0].find_all("li")[4]
#tem.a["onclick"]
#driver.find_elements_by_class_name("brgNavBar")[0].click()
#
#driver.find_element_by_id("brgNavBar")
#
#element = driver.find_elements_by_tag_name("ul")
#driver.find_element_by_xpath("//ul[@class='brgNavBar']")
#[4].a["href"]
#Final_rule_odd=soup.find_all("tr",class_="odd")
#driver.find_element_by_id("btnFinal")








































