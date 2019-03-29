# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 14:22:09 2019

@author: DongliangLu
"""

#get the content of final rules and set it as txt files
#consort to final rule dic
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import pickle
import os

import numpy as np
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import nltk
import string

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
import PyPDF2
from collections import Counter


punct=string.punctuation

stop=stopwords.words("english")
porter_stemmer = PorterStemmer()

def merge_clean(text):
    S=""
    for line in text:
        S+=line
        S+=" "
    S=" ".join([ porter_stemmer.stem(i) for i in S.lower().split() if i not in stop])
    for p in punct:
        S=S.replace(p,"")
    return S

def add_word(word, dic):
    if word in dic:
        dic[word] += 1
    else:
        dic[word] = 1
    return dic
    
def content_to_dic(content, dic):
    for w in content.split():
        dic=add_word(w, dic)
    return dic

#comments_df_old=comments_inf_df
#separate_dic=tem
#total_dic=tem
def create_dic_df(comments_df_old, separate_dic, total_dic):
    new_index=np.arange(len(separate_dic))
    new_columns=total_dic.keys()
    new_df=pd.DataFrame(index=new_index, columns=new_columns)
    new_df=new_df.fillna(0)
    
    for comment_i in range(len(separate_dic)):
        comment_dic=separate_dic[comment_i]
        for word_j in comment_dic.keys():
            new_df.loc[comment_i, word_j ]=comment_dic[word_j]

    return new_df




def pdf_parse1(path):
    S=""
    fp = open(path, 'rb') 
    praser = PDFParser(fp)
    doc = PDFDocument()
    praser.set_document(doc)
    doc.set_parser(praser)
    doc.initialize()
    fp.close()
    if not doc.is_extractable:
        return None
    else:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        page_num=0
        for page in doc.get_pages(): 
            page_num+=1
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    results = x.get_text()
                    #print(len(results))
                    try:#if it is some format notation, ignore it
                        S+=results
                        S+="\n"
                    except:
                        pass
    return S,page_num


def pdf_parse2(pdf_save_add):
    with open(pdf_save_add ,"rb") as pdfFileObj:
        pdfFileObj = open(pdf_save_add, 'rb')
    
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        N=pdfReader.numPages
        pageObj = pdfReader.getPage(0)
        S=pageObj.extractText()
    return S,N


def convery_pdf_to_txt(pdf_add):
    if ".pdf" in pdf_add:
        txt_save_add=pdf_add.replace(".pdf",".txt")
        if not os.path.exists(txt_save_add):
            with open(txt_save_add,"w") as f:
                f.write("0")
        pdf_or_not=1
        try:
            text,page_num=pdf_parse1(pdf_add)
            pdf_readable=1
        except:
            text,page_num=pdf_parse2(pdf_add)
            pdf_readable=0
        try:
            with open(txt_save_add,"w") as f:
                f.write(text.encode('latin-1', 'replace').decode("utf-8","ignore").replace("?"," "))   
        except:
            with open(txt_save_add,"w") as f:
                f.write("0")
        return pdf_or_not, pdf_readable, page_num
    else:
        return 0,0,0
    
def convery_pdf_to_txt2(pdf_add):
    txt_save_add=pdf_add.replace(".pdf",".txt")
    if not os.path.exists(txt_save_add):
        with open(txt_save_add,"w") as f:
            f.write("0")
    try:
        text,page_num=pdf_parse1(pdf_add)
        pdf_readable=1
    except:
        text,page_num=pdf_parse2(pdf_add)
        pdf_readable=0
    try:
        with open(txt_save_add,"w") as f:
            f.write(text.encode('latin-1', 'replace').decode("utf-8","ignore").replace("?"," "))   
    except:
        with open(txt_save_add,"w") as f:
            f.write("0")
            print("writing failed")
    return pdf_readable, page_num

    
    
def merge_lines(text):
    end_symbol = []
    for i in range(10):
        end_symbol.append(str(i))
    end_symbol.append(".")
    end_symbol = set(end_symbol)
#    for i in punct:
#        Number.append(i)

    text_lines=[]
    tem=""
    pre="0"
    for line in text:
#        print(line)
##        if line[0] == line[0].upper() and ( pre[-1] in end_symbol):
        if line[0] == line[0].upper():
            if pre:
                if pre[-1] in end_symbol:
                    if tem != "":
                        tem = tem.replace("\n", "")
                        text_lines.append(tem.strip())
                    tem = line
                else:
                    tem += line
            else:
#            print(pre[-1])
                if tem != "":
                    tem = tem.replace("\n", "")
                    text_lines.append(tem.strip())
                tem = line
        else:
            tem += line
        pre = line.strip()
        
    return text_lines

def scrape_number(line):
    Number = []
    for i in range(10):
        Number.append(str(i))
    Number = set(Number)    
    
    number=""
    while line[0] in Number:
        number+=line[0]
        if len(line)>1:
            line=line[1:]
        else:
            line="a"
    return number



def find_citation_location(merged_text):
    Number = []
    for i in range(10):
        Number.append(str(i))
    Number = set(Number)
    
    location_dic={}
    citation_pattern = re.compile("\.\d+")
    
    for line in merged_text:#381 is a good example
        location_span = re.search(citation_pattern,line)
        while location_span:
            location_span = location_span.span()
            start = location_span[0]
            end = location_span[1]
            location = line[start+1:end]
            citation_content = line[:end]
            if location in location_dic:
                location_dic[location].append(citation_content.strip())
            else:
                location_dic[location] = [citation_content.strip()]
            line = line[end:]
            location_span = re.search(citation_pattern,line)

    return location_dic




















with open(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw"+r"\scrape_SEC.pickle","rb") as f:
    tem=pickle.load(f, encoding='latin1')
scrape_SEC = tem    
    
basic_store_path = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw\final_rule"    

first_time = False
if first_time:
    for i in range(len(scrape_SEC)):
        directory = basic_store_path + "\\"+ str(i)
        os.mkdir(directory)  

#download file
scrape_SEC['pdf or not'] = 1
for i in range(len(scrape_SEC)):
#for i in range(125,126):    
    rule_add = scrape_SEC.loc[i,'final rule url']
    if ".pdf" not in rule_add:
        scrape_SEC.loc[i,'pdf or not'] = 0
    store_pdf_add = basic_store_path+"\\"+str(i)+"\\"+str(i)+".pdf"
    store_txt_add = store_pdf_add.replace(".pdf",".txt")
    if "pdf" in rule_add:
        if not os.path.exists(store_pdf_add):
            rule = requests.get(rule_add)
            print("downloading pdf rule for rule %i"%i)
            with open(store_pdf_add,'wb') as f: 
                f.write(rule.content)
            
    if ".htm" in rule_add:
        if not os.path.exists(store_txt_add):
            soup1 = BeautifulSoup(requests.get(rule_add).text,"lxml")
            print("downloading txt rule for rule %i"%i)
            for script in soup1(["script", "style"]):
                script.extract()  
            with open(store_txt_add,'w') as f: 
                f.write(soup1.get_text().encode('latin-1', 'replace').decode("utf-8","ignore").replace("?"," ")) 
            
        
        
        
        
#    if not os.path.exists(store_txt_add):        
        
#        not_usable=convery_pdf_to_txt(store_pdf_add )
    
#        if "pdf" in rule_add:
#            rule = requests.get(rule_add)
#            with open("python_logo.png",'wb') as f: 
#                f.write(store_pdf_add ,"wb")
            
#change file into txt
first_time_conveying = False
if first_time_conveying:
    scrape_SEC['good final rule or not'] = 1
not_successful = []
for i in range(len(scrape_SEC)):
#for i in range(125,126):
    store_pdf_add = basic_store_path+"\\"+str(i)+"\\"+str(i)+".pdf"
    store_txt_add = store_pdf_add.replace(".pdf",".txt")
    if not os.path.exists(store_txt_add):
        print("converting rule %i into txt file"%i)
        pdf_readable, page_num = convery_pdf_to_txt2(store_pdf_add)
        if (not pdf_readable) or (page_num<10):
            scrape_SEC.loc[i,'good final rule or not'] = 0
            not_successful.append(i)
        
scrape_SEC.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw"+r"\scrape_SEC.csv", index = False)
pickle.dump(scrape_SEC,open(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw"+r"\scrape_SEC.pickle","wb"))
with open(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw"+r"\scrape_SEC.pickle","rb") as f:
    tem=pickle.load(f, encoding='latin1')





























