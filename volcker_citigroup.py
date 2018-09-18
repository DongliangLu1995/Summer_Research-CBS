# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 14:37:12 2018

@author: DongliangLu
"""

#this program finds particular volcker rule and citigroup's comments

import pickle
import numpy as np
import pandas as pd
import re
import os

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string

stop=stopwords.words("english")
porter_stemmer = PorterStemmer()
punctuation=list(string.punctuation)
punctuation.append("´ ")
punctuation.append("’")


def strip_pron(org, punctuation):
#    pron=[",","'",".","´ "]
    if "&" in org:
        org = " ".join([i.strip() for i in org.split("&")])
    if "/" in org:
        org = " ".join([i.strip() for i in org.split("/")])
    for p in punctuation:
        if p in org:
            org=org.replace(p,"")
    return org


def clean_text(text, stop):
    text=text.lower()
    text=" ".join([porter_stemmer.stem(i) for i in text.split() if i not in stop])
    text=strip_pron(text, punctuation)
    return text


def remove_last(loc):
    citation_pattern = re.compile("\.\d+")
    start = re.search(citation_pattern,loc).span()[0]
    loc = loc[:start]
    return loc


def add_to_dic(dic, key,value):
    if key in dic:
        dic[key].append(value)
    else:
        dic[key] = [value]
    return dic


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
    

def content_list_to_str(content):
    content_total = ""
    for line in comment_content:
        content_total += " "
        content_total += line
    content_total = clean_text(content_total, stop)
    return content_total


def subs_score(a,b,score_match,score_notmatch):
    return score_match if a==b else score_notmatch

def find_similarity_parts(s1, s2, substi_score_m=3, substi_score_n=-3, w=2 ):

    H=np.zeros((len(s1)+1, len(s2)+1) )
    n,m=H.shape
    for i in range(1,n):
        for j in range(1,m):
            score1 = H[i-1,j-1] + subs_score(s1[i-1],s2[j-1],substi_score_m,substi_score_n)
            score2 = H[i-1,j] - w
            score3 = H[i,j-1] - w
            score4 = 0
            H[i,j] = max(score1,score2,score3,score4)
    
    #trace back
    trace_back_index=[]
    max_index=np.where(H==np.max(H))
    r_index=max_index[0][0]
    c_index=max_index[1][0]
    trace_back_index.append( (r_index, c_index) )
    score_now=np.max(H)
    while score_now >0:
        score1=H[r_index-1,c_index-1]
        score2=H[r_index-1,c_index]
        score3=H[r_index,c_index-1]
        score_now=max(score1,score2,score3)
        if max(score1,score2,score3)==score1:#what about the same score
            r_index-=1
            c_index-=1
        elif max(score1,score2,score3)==score2:
            r_index-=1
        else:
            c_index-=1
        trace_back_index.append( (r_index,c_index) )
            
    #print
    share=""
    s1_fraction_index=[]
    s2_fraction_index=[]
    for i in range(len(trace_back_index)-1):
        if not s1_fraction_index or s1_fraction_index[-1] !=trace_back_index[i][0]:
            s1_fraction_index.append( trace_back_index[i][0] )
        if not s2_fraction_index or s2_fraction_index[-1] !=trace_back_index[i][1]:
            s2_fraction_index.append( trace_back_index[i][1] )
            
            
    s1_takeout=" ".join([s1[i-1] for i in s1_fraction_index][::-1])
    s2_takeout=" ".join([s2[i-1] for i in s2_fraction_index][::-1])
#    print(s1_takeout)
#    print(s2_takeout)
    return s1_takeout, s2_takeout









rule_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\final rule\SEC_rule\final\10.txt"

comment_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\download\SEC_comments\rule_1\Citigroup_1.txt"

with open(rule_add, 'r') as f:
    rule_content_raw = f.readlines()
    
with open(comment_add, 'r') as f:
    comment_content_raw = f.readlines()
    
    

comment_content = get_rid_of_one_word_and_citation_sentence(comment_content)
























