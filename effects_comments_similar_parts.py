# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 14:01:03 2018

@author: DongliangLu
"""

#compare lobbying effects with original comments

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



from heapq import heappush, heappop
def minDistance(word1, word2):
    """
    :type word1: str
    :type word2: str
    :rtype: int
    """
    heap = [(0, word1, word2)]
    visited = set()
    while heap:
        d, w1, w2 = heappop(heap)
        if (w1, w2) in visited:
            continue
        visited.add((w1, w2))    
        if w1 == w2:
            return d
        if w1 and w2 and w1[0] == w2[0]:
            heappush(heap, (d, w1[1:], w2[1:]))
        else:
            if w1: heappush(heap, (d+1, w1[1:], w2)) #delete
            if w1 and w2: heappush(heap, (d+1, w1[1:], w2[1:])) #replace
            if w2: heappush(heap, (d+1, w1, w2[1:])) #add


def find_match_score(s1, s2, high, low):
    l1 = len(s1)
    l2 = len(s2)
    
    if l1>l2:
        s1, s2 = s2, s1
        l1, l2 = l2, l1
    #keep s1 be the shorter one
    if s1[0] != s2[0]:
        percent = 0
    else:
        percent = 1 - minDistance(s1, s2)/l2
        
        
    score = low + percent*(high - low)
    return score





def find_similarity_parts(s1, s2, substi_score_m=3, substi_score_n=-3, w=2 ):

    H=np.zeros((len(s1)+1, len(s2)+1) )
    n,m=H.shape
    for i in range(1,n):
        for j in range(1,m):
            score1 = H[i-1,j-1] + find_match_score(s1[i-1],s2[j-1],substi_score_m,substi_score_n)
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










#final_rule_good = [0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]
result_fold_basic = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\similar_paragraph_2\result"
#for i in final_rule_good:
#    result_rule_path = result_fold_basic+"\\"+str(i)
#    if os.path.exists(result_rule_path):
#        pass
#    else:
#        os.mkdir(result_rule_path)

lobby_sentence_related_org_save_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\similar_paragraph_2"
comments_save_basic_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\download\SEC_comments"
substi_score_m = 5#ai=bj
substi_score_n = -2#ai!=bj
w=2 #penalty

final_rule_good = [0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]
#final_rule_good = [10]
final_rule_good = [6]
#final_rule_good = [2]
#rule_type_i = 10
for rule_type_i in final_rule_good: 
    
    print("now dealling with rule type: "+str(rule_type_i))
    result_add = result_fold_basic+"\\"+str(rule_type_i)+"_result.txt"
    
    lobby_sentence_related_org_save_add_i = lobby_sentence_related_org_save_add + "\\lobby_org" + str(rule_type_i) + ".pickle"
    
    with open(lobby_sentence_related_org_save_add_i,"rb") as f:
        tem=pickle.load(f)  
    lobby_sentence_related_org = tem

    
    #get the comment file add for each organization
    comment_fold = comments_save_basic_add+"\\rule_"+str(rule_type_i)
    orgs_comments_dic={}
    for comment in os.listdir(comment_fold):
        if ".txt" in comment:
            org_name = comment.split("_")[0]
            comment_add = comment_fold+"\\"+comment
            orgs_comments_dic = add_to_dic(orgs_comments_dic,org_name,comment_add)
    
    if rule_type_i==10:
        comment_fold2 = comments_save_basic_add+"\\rule_"+str(1)
        for comment in os.listdir(comment_fold2):
            if ".txt" in comment:
                org_name = comment.split("_")[0]
                comment_add = comment_fold2+"\\"+comment
                orgs_comments_dic = add_to_dic(orgs_comments_dic,org_name,comment_add)

    
    
    
    org_comment_text_clean_dic={}
    for org in orgs_comments_dic.keys():
        comment_file_list = orgs_comments_dic[org]
        comment_content = []
        for comment_file in comment_file_list:
            with open(comment_file, 'r') as f:
                text = f.readlines()
            comment_content.extend(text)
        comment_content = get_rid_of_one_word_and_citation_sentence(comment_content)
    #    merged_content = merge_lines(comment_content)
        if comment_content:
    #        merged_content = merge_lines(comment_content)
            content_total = content_list_to_str(comment_content)
            org_comment_text_clean_dic[org] = content_total    
    
#    org_comment_text_clean_dic stores the text of the comments of the orgs
    
    #get lobbying result and its related organizations
    
    for l_i in range(0, len(lobby_sentence_related_org)):
        print("now dealing with result "+str(l_i))
        lobby_result = lobby_sentence_related_org[l_i][0]
        lobby_result_clean = clean_text(lobby_result, stop)
        related_orgs = lobby_sentence_related_org[l_i][1]
        
        for org in related_orgs:
            if org in org_comment_text_clean_dic:
                comment_clean = org_comment_text_clean_dic[org]
                similar_1, similar_2 = find_similarity_parts(lobby_result_clean.split(), comment_clean.split(), substi_score_m, substi_score_n, w )
                print("result num:" + str(l_i))
                print(similar_1)
#                            print("\n")
                print(similar_2)
                print("\n")
                with open(result_add,"a") as f:
                    f.write("organization: " + org)
                    f.write("\n")
                    f.write("lobby result num:" + str(l_i))
                    f.write("\n")
                    f.write(similar_1)
                    f.write("\n")
                    f.write(similar_2)
                    f.write("\n")
        
    
    
    