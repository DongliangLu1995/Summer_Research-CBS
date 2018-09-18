# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 14:30:40 2018

@author: DongliangLu
"""

#toy example

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import pickle

def distance(c1,c2):
    #c1,c2 is np.array
    a1=np.sum(c1**2)
    a2=np.sum(c2**2)
    if a1!=0 and a2!=0:
        return  np.sqrt( 1 - np.sum( c1*c2 )**2  / (a1 * a2 ) )
    else:
        return np.nan



def cal_distance_matrix(comment_feature_array):
    
    r,c = comment_feature_array.shape
    m = np.zeros([r,r])
    for row_i in range(r):
        for col_j in range(row_i, r):
            m[row_i, col_j]=distance(comment_feature_array[row_i],comment_feature_array[col_j])
            m[col_j, row_i] = m[row_i, col_j]
    return m



def calculate_similarity_count(comment_dic_array,i,j):
    #input should be an array, not a df, and it should be count
#    comment_dic_array=comment_dic.values
    return np.sum(comment_dic_array[i]*comment_dic_array[j]) / np.sqrt(np.sum(comment_dic_array[i]**2))/np.sqrt(np.sum(comment_dic_array[j]**2))
    
def calculate_similarity_set(comment_dic_set_array,i,j):
    #input should be an array, and should be set
#    r,c = comment_dic_array.shape
#    comment_dic_set_array=np.ones([r,c]) * (comment_dic_array != 0)
    return np.sum(comment_dic_set_array[i]*comment_dic_set_array[j]) / np.sqrt(np.sum(comment_dic_set_array[i]))/np.sqrt(np.sum(comment_dic_set_array[j]))
     
def calculate_similarity_tfidf(comment_dic_array,i,j):
    #input should be an array, and should be count
    return np.sum(comment_dic_array[i]*comment_dic_array[j]) / np.sqrt(np.sum(comment_dic_array[i]**2))/np.sqrt(np.sum(comment_dic_array[j]**2))


def cal_similarity_matrix(comment_dic_array, method):
#    comment_dic_array = comment_dic.values
    r,c = comment_dic_array.shape
    m = np.zeros([r,r])
    if method == "count":
        for row_i in range(r):
            for col_j in range(row_i, r):
                m[row_i, col_j]=calculate_similarity_count(comment_dic_array,row_i,col_j)
                m[col_j, row_i] = m[row_i, col_j]
    elif method == "set":
        for row_i in range(r):
            for col_j in range(row_i, r):
                m[row_i, col_j]=calculate_similarity_set(comment_dic_array,row_i,col_j)
                m[col_j, row_i] = m[row_i, col_j]
    elif method == "tfidf":
        for row_i in range(r):
            for col_j in range(row_i, r):
                m[row_i, col_j]=calculate_similarity_tfidf(comment_dic_array,row_i,col_j)
                m[col_j, row_i] = m[row_i, col_j]
    return m

def cal_distance_matrix(comment_feature_array):
    
    r,c = comment_feature_array.shape
    m = np.zeros([r,r])
    for row_i in range(r):
        for col_j in range(row_i, r):
            m[row_i, col_j]=distance(comment_feature_array[row_i],comment_feature_array[col_j])
            m[col_j, row_i] = m[row_i, col_j]
    return m


def merge_clean(text):
    S=text
    for p in punct:
        S=S.replace(p,"")
    S=" ".join([ porter_stemmer.stem(i) for i in S.lower().split() if i not in stop])

    return S

def content_to_dic(content, dic):
    for w in content.split():
        dic=add_word(w, dic)
    return dic


def merge_two_dic(dic1, dic2):
    merge_dic={}
    for key in dic1.keys():
        if key in dic2.keys():
            merge_dic[key] = dic1[key] + dic2[key]
        else:
            merge_dic[key] = dic1[key]
    for key in dic2.keys():
        if key in merge_dic:
            pass
        else:
            merge_dic[key]=dic2[key]
    return merge_dic

def add_word(word, dic):
    if word in dic:
        dic[word] += 1
    else:
        dic[word] = 1
    return dic


from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string

punct=string.punctuation

stop=stopwords.words("english")
porter_stemmer = PorterStemmer()



final_rule = "It is required that the trading desk or other organizational unit's market making-related activities be designed not to exceed the reasonably expected near term demands of clients, customers, or counterparties. "



final_rule = merge_clean(final_rule)
final_rule_dic = {}
final_rule_dic = content_to_dic(final_rule, final_rule_dic)

comments=[0,1,2,3]
comments[0] = "Trading desks should not be constrained to much by clients or customers, this will greatly stop the desks from making more profits for them."

comments[1] = "Private funds should have more freedoms on proprietary trading than banks since they are not the cause of the financial crisis."

comments[2] = "I also think that Private funds should have more freedoms on proprietary trading activities.    "

comments[3] = "I think the banks and pravite funds should not have any freedom to do any trading to prevent next financial crisis."

comments_dic_list=[]
for i in range(len(comments)):
    comments[i] = merge_clean(comments[i])
    new_dic={}
    comments_dic_list.append(content_to_dic(comments[i], new_dic))

comments_dic_list.append(final_rule_dic)

p = pd.DataFrame(comments_dic_list)
p = p.fillna(0)
p = p.values

for i in range(4):
    print( calculate_similarity_set(p,i,-1))

m = cal_distance_matrix(p[:-1])
print(m.mean(axis = 1))