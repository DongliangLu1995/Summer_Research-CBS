# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 22:37:32 2019

@author: DongliangLu
"""
#get basic inf of final rules, comments, 
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import pickle



years_url_list1 = []
years_url_list2 = []
basic_url = r"https://www.sec.gov/rules/final.shtml"
#years_url_list.append(basic_url)
basic_url1 = r"https://www.sec.gov/rules/final/finalarchive/finalarchive"
#1998-2015
#[2006-2015]
#[1998-2006] different format
for i in range(2015,2005,-1):
#    print(i)
    years_url_list1.append(basic_url1 + str(i) +".shtml")
for i in range(2005,1997,-1):
#    print(i)
    years_url_list2.append(basic_url1 + str(i) +".shtml")
#years_url_list.append()

#url_dic_list = []
#soup = BeautifulSoup(requests.get(basic_url).text,"lxml")
#link_years = soup.find_all("p", id="archive-links")[0]
#years_url_list_raw = link_years.find_all("a")
#for i in range(len(years_url_list_raw)):
#    url_href = years_url_list_raw[i]
#
#url = years_url_list[0]
#soup_basic = BeautifulSoup(requests.get(url).text,"lxml")
##soup1 = soup_basic.find_all("td",valign = "top")
#soup1 = soup_basic.find_all("tr")
#soup2 = []
#for soup in soup1:
#    if soup.text.count("omment") == 1:
#        soup2.append(soup)
#
#soup3 = soup2[1]
##soup4 = soup3.find_all("td",valign = "top", nowrap="")
#soup4 = soup3.find_all("td",valign = "top")
#date = soup4[1].text
#soup5 = soup4[2].find_all("a")
#for soup in soup5:
#    if "PDF" in soup.text:
#        url_final_rule = soup.get("href")
#    if "omment" in soup.text:
#        comment_url = r"https://www.sec.gov" + soup.get("href")
#url_dic_list.append({})
#url_dic_list[-1]["date"] = date
#url_dic_list[-1]["final rule url"] = url_final_rule
#url_dic_list[-1]["comment url"] = comment_url


url_dic_list = []
bad_url = []
#url = "https://www.sec.gov/rules/final/finalarchive/finalarchive2005.shtml"
#2011 and before had some difference for final rule
#comments for 2010.12.28 is true, the name is strange
#comments for 2012.8.22 is also true, the name is strange, and it has several comments
for url in years_url_list1:
    print()
    print("now in web: "+url)
    soup_basic = BeautifulSoup(requests.get(url).text,"lxml")
    
    soup1 = soup_basic.find_all("tr")#all final rule url
    soup2 = []#final rule url has comments
    comment_ind = 0
    for soup in soup1:
        if soup.text.count("omment") >= 1:
            if comment_ind >0:
                soup2.append(soup)
            else:
                comment_ind +=1
#    tem = []            
#    for soup in soup1:
#        if soup.text.count("omment") >= 1:
#            tem.append(soup)
        
    for soup3 in soup2:#each rule
        try:
    #        soup3 = soup2[0]
    #        soup4 = soup3.find_all("td",valign = "top", nowrap="")
            soup4 = soup3.find_all("td",valign = "top")#date
            date = soup4[1].text
            soup5 = soup4[2].find_all("a")#href of rule
            find_final_ind = 0
            rule_name = soup4[2].text.split("\n")[0]

            for soup_i in range(len(soup5)):
                soup = soup5[soup_i]
                if soup_i == 0:
                    url_proposed_rule = soup.get("href")
                if "PDF" in soup.text:#find final rule of federal register version pdf
                    if ".pdf" in soup.get("href"):
                        url_final_rule = soup.get("href")
                        find_final_ind = 1
                if 'Federal Register version' in soup.text:
                    url_final_rule_backup = r"https://www.sec.gov" + soup.get("href")
                if "omment" in soup.text:
                    comment_url = r"https://www.sec.gov" + soup.get("href")
#            if url_final_rule or url_final_rule_backup:
            url_dic_list.append({})
            url_dic_list[-1]["rule name"] = rule_name
            url_dic_list[-1]["date"] = date
            url_dic_list[-1]["final rule url"] = url_final_rule if find_final_ind == 1 else url_final_rule_backup
            url_dic_list[-1]["proposed rule url"] = url_proposed_rule
            url_dic_list[-1]["comment url"] = comment_url
            
            
            print("date: "+date)
            print("final url: "+url_final_rule)
            print("proposed url: "+url_proposed_rule)
            print("comment url: "+comment_url)
        except:
            bad_url.append(soup3)
            
#yearlist1 done


            
url_dic_list2 = []
bad_url2 = []
#comments right, although weird
#2003.6.16
for url in years_url_list2:
    print()
    print("now in web: "+url)
    soup_basic = BeautifulSoup(requests.get(url).text,"lxml")
    
    soup1 = soup_basic.find_all("tr")#all final rule url
    soup2 = []#final rule url has comments
    comment_ind = 0
    for soup in soup1:
        if soup.text.count("omment") >= 1:
            if comment_ind >0:
                soup2.append(soup)
            else:
                comment_ind +=1
#    tem = []            
#    for soup in soup1:
#        if soup.text.count("omment") >= 1:
#            tem.append(soup)
        
    for soup3 in soup2:#each rule
        try:
    #        soup3 = soup2[0]
    #        soup4 = soup3.find_all("td",valign = "top", nowrap="")
            soup4 = soup3.find_all("td",valign = "top")#date
            date = soup4[1].text
            soup5 = soup4[2].find_all("a")#href of rule
            rule_name = soup4[2].text.split("\n")[0]
            find_final_ind = 0
            url_final_rule_backup = ""
            url_final_rule_backup2 = ""
            url_final_rule = ""
            for soup_i in range(len(soup5)):
                soup = soup5[soup_i]
                if soup_i == 0:
                    url_proposed_rule = soup.get("href")
                if "PDF" in soup.text:#find final rule of federal register version pdf
                    if ".pdf" in soup.get("href"):
                        url_final_rule = soup.get("href")
                        find_final_ind = 1
                        if "https:" not in url_final_rule:
                            url_final_rule = r"https://www.sec.gov"+ soup.get("href")
                if 'Federal Register version' in soup.text:
                    url_final_rule_backup = r"https://www.sec.gov" + soup.get("href")
                if "omment" in soup.text:
                    comment_url = r"https://www.sec.gov" + soup.get("href")
                if "final" in soup.get("href"):
                    if "https:" not in soup.get("href"):
                        url_final_rule_backup2 = r"https://www.sec.gov"+ soup.get("href")
                    else:
                        url_final_rule_backup2 = soup.get("href")
                    
            if url_final_rule or url_final_rule_backup or url_final_rule_backup2:
                url_dic_list2.append({})
                url_dic_list2[-1]["date"] = date
                url_dic_list2[-1]["rule name"] = rule_name
                if find_final_ind == 1:
                    url_dic_list2[-1]["final rule url"] = url_final_rule
                else:
                    if url_final_rule_backup:
                        url_dic_list2[-1]["final rule url"] = url_final_rule_backup
                    else:
                        url_dic_list2[-1]["final rule url"] = url_final_rule_backup2
                url_dic_list2[-1]["proposed rule url"] = url_proposed_rule
                url_dic_list2[-1]["comment url"] = comment_url
                
                print("date: "+date)
                print("final url: "+url_final_rule)
                print("proposed url: "+url_proposed_rule)
                print("comment url: "+comment_url)
        except:
            bad_url.append(soup3)





    
url_dic_list.extend(url_dic_list2)
scrape_SEC=pd.DataFrame(url_dic_list)
scrape_SEC.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw"+r"\scrape_SEC.csv", index = False)
pickle.dump(scrape_SEC,open(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw"+r"\scrape_SEC.pickle","wb"))
with open(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw"+r"\scrape_SEC.pickle","rb") as f:
    tem=pickle.load(f, encoding='latin1')


















