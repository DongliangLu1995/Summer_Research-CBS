# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 10:12:05 2019

@author: DongliangLu
"""

#download meeting and comments's information
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import pickle
import os


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
                if find_memo(meetings[l-1]):
                    return l-1
                return l#if not have any meetings, return none
    return i

def grab_org(meeting_inf):
    start=meeting_inf.find("call with")
    if start!=-1:
        meeting_inf=meeting_inf[start+10:]
    elif meeting_inf.find("calls with")!=-1:
        start=meeting_inf.find("calls with")
        meeting_inf=meeting_inf[start+11:]
    elif meeting_inf.find("Calls with")!=-1:
        start=meeting_inf.find("Calls with")
        meeting_inf=meeting_inf[start+11:]
    elif meeting_inf.find("Call with")!=-1:
        start=meeting_inf.find("Call with")
        meeting_inf=meeting_inf[start+10:]
    elif meeting_inf.find("Meeting with")!=-1:
        start=meeting_inf.find("Meeting with")
        meeting_inf=meeting_inf[start+13:]
    elif meeting_inf.find("converstation with")!=-1:
        start=meeting_inf.find("converstation with")
        meeting_inf=meeting_inf[start+19:]
    elif meeting_inf.find("Converstation with")!=-1:
        start=meeting_inf.find("Converstation with")
        meeting_inf=meeting_inf[start+19:]
    
    else:
        start=meeting_inf.find("meeting with")
        meeting_inf=meeting_inf[start+13:]
    return meeting_inf

def org_strip(org):
    org=org.replace("Counsel for ", "")
    org=org.replace("a representative of ","")
    org=org.replace("representatives of ","")
    org=org.replace("representatives from ","")
    org=org.replace("Representatives from ","")
    org=org.replace("Representatives of ","")
    return org

def org_stripdate(org):
    pattern = re.compile("dated")
    if pattern.search(org):
        end = pattern.search(org).span()[0]
        org = org[:end]
        return org.strip().rstrip(",")
    else:
        org = ",".join(org.split(",")[:-2])
        return org.strip().rstrip(",")

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

def grab_org_c_2(comment_inf):
    comment_inf = ",".join(comment_inf.split(",")[:-2])
    if "Comments of " in comment_inf:
        comment_inf = comment_inf.replace("Comments of ","")
    return comment_inf.strip()
        
        
        
def find_all_related_comments(all_url):
    url = all_url[-1]
    soup_basic = BeautifulSoup(requests.get(url).text,"lxml")
    if soup_basic.find_all("p"):
        for soup in soup_basic.find_all("p"):
            if "See also:" in soup.text:
                url_new = r"https://www.sec.gov"+soup.a['href']
                if url_new in all_url:
                    return all_url
                else:
                    all_url.append(url_new)
                    return find_all_related_comments(all_url)
            else:
                return all_url
    else:
        return all_url







with open(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw"+r"\scrape_SEC.pickle","rb") as f:
    tem=pickle.load(f, encoding='latin1')
scrape_SEC = tem    
    
basic_store_path = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw\comment_meeting_inf"    

first_time = False
if first_time:
    for i in range(len(scrape_SEC)):
        directory = basic_store_path + "\\"+ str(i)
        os.mkdir(directory)  

basic_url_comment_meeting = r"https://www.sec.gov"
comment_list_total = []
meeting_list_total = []
#76 or higher is different
#4 has comments on more than one page
#for i in range(len(scrape_SEC)):
#40 type letter
#116 someting weird
#64,66 weird
#73 old
for i in range(0,76):
    comment_list = []
    meeting_list = []
    print("scrape comment and meeting inf for rule %i "%i)
    
    comment_mother_url_list = find_all_related_comments([scrape_SEC.loc[i,'comment url']])
    for comment_mother_url in comment_mother_url_list:

    
        soup_basic = BeautifulSoup(requests.get(comment_mother_url).text,"lxml")
        comment_meeting = soup_basic.find_all("tr",onmouseover="this.bgcolor='#E0E0E0'")
        comment_meeting2 = soup_basic.find_all("tr",onmouseover="this.bgColor='#E0E0E0'")
        comment_meeting.extend(comment_meeting2)
        type_letter = soup_basic.find_all("td",colspan="2")
        if type_letter:
            for letter in type_letter:
                if "Type" in letter.text:
                    comment_list.append({})
                    comment_list[-1]["date"] = 'Jan 1, 1900'
                    comment_list[-1]["people"] = "Individual"
                    comment_list[-1]["url"] = basic_url_comment_meeting + letter.a['href']
                    comment_list[-1]["rule type"] = i
                    comment_list[-1]['comment num'] = letter.text.split()[-1]
        
        for i_inf in range(0, len(comment_meeting)):
            try:
                meeting_inf = comment_meeting[i_inf].a.text
                
                if "Memorandum" in meeting_inf:
                        meeting_inf = comment_meeting[i_inf].a.text
                        pdf_url = basic_url_comment_meeting+comment_meeting[i_inf].a["href"]
                        dates = grab_date(meeting_inf)
                    #    if not dates:
                    #        print(meeting_inf)
                        for date in dates:
                            meeting_list.append({})
                            meeting_list[-1]["date"]=date
                            org=grab_org(meeting_inf)
                            org=org_strip(org)
                            meeting_list[-1]["organization"]=org
                            meeting_list[-1]["url"]=pdf_url
                            meeting_list[-1]["rule type"]=i
                else:
                    comment_content = comment_meeting[i_inf].text
                    
                    date = grab_date_c(comment_content)
                    people = " ".join(comment_content.split()[3:])
                    comment_url = basic_url_comment_meeting+comment_meeting[i_inf].a["href"]
                    if ".pdf" in comment_url:
                        pdf_or_not_comment = 1
                    else:
                        0
                #    if not dates:
                #        print(meeting_inf)
            
                    comment_list.append({})
                    comment_list[-1]["date"] = date
                    comment_list[-1]["people"] = people
                    comment_list[-1]["url"] = comment_url
                    comment_list[-1]["rule type"] = i
                    comment_list[-1]['comment num'] = 1
                    comment_list[-1]['pdf or not'] = pdf_or_not_comment
            except:
                pass
            
    comment_list_total.extend(comment_list)
    meeting_list_total.extend(meeting_list)
    
    comment_df = pd.DataFrame(comment_list)
    meeting_df = pd.DataFrame(meeting_list)
    store_path_c = basic_store_path+"\\"+str(i)+"\\"+str(i)+"_c.pickle"
    store_path_m = basic_store_path+"\\"+str(i)+"\\"+str(i)+"_m.pickle"
    pickle.dump(comment_df,open(store_path_c,"wb"))
    pickle.dump(meeting_df,open(store_path_m,"wb"))
    comment_df.to_csv(store_path_c.replace(".pickle",".csv"),index = False)
    meeting_df.to_csv(store_path_m.replace(".pickle",".csv"),index = False)
    



#for i in range(106,len(scrape_SEC)):
for i in range(76,len(scrape_SEC)+1):
    if i==len(scrape_SEC):
        i=73
    comment_list = []
    meeting_list = []
    print("scrape comment and meeting inf for rule %i "%i)
    
    comment_mother_url_list = find_all_related_comments([scrape_SEC.loc[i,'comment url']])
    for comment_mother_url in comment_mother_url_list:

    
        soup_basic = BeautifulSoup(requests.get(comment_mother_url).text,"lxml")
        comment_meeting = soup_basic.find_all('li')
        type_letter = soup_basic.find_all("td",colspan="2")
        if type_letter:
            for letter in type_letter:
                if "Type" in letter.text:
                    comment_list.append({})
                    comment_list[-1]["date"] = 'Jan 1, 1900'
                    comment_list[-1]["people"] = "Individual"
                    comment_list[-1]["url"] = basic_url_comment_meeting + letter.a['href']
                    comment_list[-1]["rule type"] = i
                    comment_list[-1]['comment num'] = letter.text.split()[-1]
        
        for i_inf in range(0, len(comment_meeting)):
            try:
                meeting_inf = comment_meeting[i_inf].text
                
                if "Memorandum" in meeting_inf:
                        meeting_inf = comment_meeting[i_inf].text
                        pdf_url = basic_url_comment_meeting+comment_meeting[i_inf].a["href"]
                        dates = grab_date(meeting_inf)
                        date = dates[-1]
                        meeting_list.append({})
                        meeting_list[-1]["date"]=date
                        org=grab_org(meeting_inf)
                        org=org_strip(org)
                        org=org_stripdate(org)
                        meeting_list[-1]["organization"]=org
                        meeting_list[-1]["url"]=pdf_url
                        meeting_list[-1]["rule type"]=i
                        
                        
                    #    if not dates:
                    #        print(meeting_inf)
#                        for date in dates:
#                            meeting_list.append({})
#                            meeting_list[-1]["date"]=date
#                            org=grab_org(meeting_inf)
#                            org=org_strip(org)
#                            meeting_list[-1]["organization"]=org
#                            meeting_list[-1]["url"]=pdf_url
#                            meeting_list[-1]["rule type"]=i
                else:
                    comment_content = comment_meeting[i_inf].text
                    
                    date = grab_date(comment_content)
                    people = grab_org_c_2(comment_content)
                    comment_url = basic_url_comment_meeting+comment_meeting[i_inf].a["href"]
                    if ".pdf" in comment_url:
                        pdf_or_not_comment = 1
                    else:
                        0
                #    if not dates:
                #        print(meeting_inf)
            
                    comment_list.append({})
                    comment_list[-1]["date"] = date[0]
                    comment_list[-1]["people"] = people
                    comment_list[-1]["url"] = comment_url
                    comment_list[-1]["rule type"] = i
                    comment_list[-1]['comment num'] = 1
                    comment_list[-1]['pdf or not'] = pdf_or_not_comment
            except:
                pass
            
    comment_list_total.extend(comment_list)
    meeting_list_total.extend(meeting_list)
    
    comment_df = pd.DataFrame(comment_list)
    meeting_df = pd.DataFrame(meeting_list)
    store_path_c = basic_store_path+"\\"+str(i)+"\\"+str(i)+"_c.pickle"
    store_path_m = basic_store_path+"\\"+str(i)+"\\"+str(i)+"_m.pickle"
    pickle.dump(comment_df,open(store_path_c,"wb"))
    pickle.dump(meeting_df,open(store_path_m,"wb"))
    comment_df.to_csv(store_path_c.replace(".pickle",".csv"),index = False)
    meeting_df.to_csv(store_path_m.replace(".pickle",".csv"),index = False)

#comment_df = pd.DataFrame(comment_list)
#meeting_df = pd.DataFrame(meeting_list)
comment_total_df = pd.DataFrame(comment_list_total)
meeting_total_df = pd.DataFrame(meeting_list_total)

store_path_c_t = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw"+"\\comment_inf.pickle"
store_path_m_t = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw"+"\\meeting_inf.pickle"
pickle.dump(comment_total_df,open(store_path_c_t,"wb"))
pickle.dump(meeting_total_df,open(store_path_m_t,"wb"))
comment_total_df.to_csv(store_path_c_t.replace(".pickle",".csv"),index = False)
meeting_total_df.to_csv(store_path_m_t.replace(".pickle",".csv"),index = False)






#   meeting_start = find_meeting_index(comment_meeting)
#    for i_inf in range(meeting_start, len(comment_meeting)):
#        meeting_inf = comment_meeting[i_inf].a.text
#        pdf_url = basic_url_comment_meeting+comment_meeting[i_inf].a["href"]
#        dates = grab_date(meeting_inf)
#    #    if not dates:
#    #        print(meeting_inf)
#        for date in dates:
#            meeting_list.append({})
#            meeting_list[-1]["date"]=date
#            org=grab_org(meeting_inf)
#            org=org_strip(org)
#            meeting_list[-1]["organization"]=org
#            meeting_list[-1]["url"]=pdf_url
#            meeting_list[-1]["rule type"]=i
#            
#    for i_inf in range(0, meeting_start):
#        comment_content = comment_meeting[i_inf].text
#        date = grab_date_c(comment_content)
#        people = " ".join(comment_content.split()[3:])
#        comment_url = basic_url_comment_meeting+comment_meeting[i_inf].a["href"]
#    #    if not dates:
#    #        print(meeting_inf)
#
#        comment_list.append({})
#        comment_list[-1]["date"]=date
#        comment_list[-1]["people"]=people
#        comment_list[-1]["url"]=comment_url
#        comment_list[-1]["rule type"]=i














