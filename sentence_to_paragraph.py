# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 22:29:26 2018

@author: DongliangLu
"""

#this program merge the sentence in the pdf final rules to paragraphs


# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 12:11:14 2018

@author: DongliangLu
"""

import numpy as np
import pandas as pd
import re

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
import PyPDF2

from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string

import string
from collections import Counter
import os
import pickle



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
    
    
def get_rid_of_one_word_and_citation_sentence(text):
    text_new=[]
    citation_pattern = re.compile("\d+\s+[A-Z]")
    for line in text:
        if len(line.split())<=1 and line[-1]!=".":
            pass
        else:
            line = line.strip()
            if re.match(citation_pattern, line):
                pass
            else:
                text_new.append(line)
    return text_new
    
    



def merge_lines(text):
    end_symbol = []
    for i in range(10):
        end_symbol.append(str(i))
    end_symbol.append(".")
    end_symbol = set(end_symbol)

    text_lines=[]
    tem=""
    pre="0"
    for line in text:
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

#    for line in merged_text:
#        line_list = line.split(".")
#        if len(line_list)>1:
#            for small_line_i in range(len(line_list)-1):
#                if line_list[small_line_i+1]:
#                    if line_list[small_line_i+1][0] in Number:
#                        location = scrape_number(line_list[small_line_i+1])
#                        if location in location_dic:
#                            location_dic[location].append(line_list[small_line_i])
#                        else:
#                            location_dic[location] = [line_list[small_line_i]]
                    
    return location_dic






first_time = False


final_rule_good=[0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]
final_rule_good=[2]

final_rule_basic_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\final rule\SEC_rule\final"
bag_of_words_save_basic_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\bag_of_words\Rule\One"
citation_location_basic_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\citation_location"

for rule_type_i in final_rule_good:
    
    final_rule_add = final_rule_basic_add + "\\" + str(rule_type_i) +".pdf"
    if first_time:
        not_usable=convery_pdf_to_txt(final_rule_add)
    final_rule_txt_add = final_rule_add.replace(".pdf", ".txt")
    bag_of_word_final_rule={}
    with open(final_rule_txt_add, 'r') as f:
        text = f.readlines()
    
    Content = merge_clean(text)
    Content_words_dic={}
    Content_words_dic = content_to_dic(Content, Content_words_dic)
    rule_comment_word_dic = content_to_dic(Content, bag_of_word_final_rule)
    
    rule_bag_of_word_save_add = bag_of_words_save_basic_add + "\\rule_word_dic_"+str(rule_type_i) +".pickle"
#    pickle.dump(rule_comment_word_dic,open(rule_bag_of_word_save_add,"wb"))

    merged_text = merge_lines(text)
    citation_dic = find_citation_location(merged_text)
    
    text_new = get_rid_of_one_word_and_citation_sentence(text)
    
    citation_location_save_add = citation_location_basic_add + "\\rule_citation_location_dic_"+str(rule_type_i) +".pickle"
#    pickle.dump(citation_dic,open(citation_location_save_add,"wb"))



#42

#with open(citation_location_save_add,"rb") as f:
#    tem=pickle.load(f)







##
#for i in range(400,500):
#    print(text[i])














#citation_pattern=re.compile("\n\d+\s+[A-Za-z]")



















 