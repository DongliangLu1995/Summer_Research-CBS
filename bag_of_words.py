# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 23:47:22 2018

@author: DongliangLu
"""

#extract bags of words from comment's txt
import pandas as pd
import numpy as np
import pickle

from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string

import string
from collections import Counter
import os
import pickle

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer


punct=string.punctuation

stop=stopwords.words("english")
porter_stemmer = PorterStemmer()

def merge_clean(text):
    S=""
    for line in text:
        S+=line
        S+=" "
    tem=S.lower().split()
    word_num=len(tem)
    S=" ".join([ porter_stemmer.stem(i) for i in tem if i not in stop])
    for p in punct:
        S=S.replace(p,"")
    return S, word_num

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
#def create_dic_df(comments_df_old, separate_dic, total_dic):
#    new_index=np.arange(len(separate_dic))
#    new_columns=total_dic.keys()
#    new_df=pd.DataFrame(index=new_index, columns=new_columns)
#    new_df=new_df.fillna(0)
#    
#    for comment_i in range(len(separate_dic)):
#        comment_dic=separate_dic[comment_i]
#        for word_j in comment_dic.keys():
#            new_df.loc[comment_i, word_j ]=comment_dic[word_j]

#    return new_df
    


scrape_result_basic_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\scrape_comment_result_SEC"
bag_of_words_save_basic_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\bag_of_words\one"
bag=["One","Two",""]


final_rule_good=[0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]
#final_rule_good=[0]
#rule_type_i=0
#final_rule_good=[10]

for rule_type_i in range(0,38):
    if rule_type_i==1:
        scrape_result_save_pickle_add = scrape_result_basic_add + "\\" +str(rule_type_i) +".pickle"
        with open(scrape_result_save_pickle_add,"rb") as f:
            tem=pickle.load(f, encoding='latin1')
        df_concat=tem
    if rule_type_i in final_rule_good:
        print(rule_type_i)
        scrape_result_save_pickle_add = scrape_result_basic_add + "\\" +str(rule_type_i) +".pickle"
        with open(scrape_result_save_pickle_add,"rb") as f:
            tem=pickle.load(f, encoding='latin1')
        comments_inf_df=tem
        if rule_type_i==10:
            comments_inf_df = comments_inf_df.append(df_concat)
            comments_inf_df=comments_inf_df.reset_index(drop= True)
        
        comments_inf_df['comment len'] = 0
        
        rule_comment_word_dic={}#total
        bag_of_word_one_list=[]#separate
        for i in range(len(comments_inf_df)):
            print("dealing with comments"+str(i))
            comment_add = comments_inf_df.loc[i,'file name']
            comment_add = comment_add.replace(".pdf",".txt")
            with open(comment_add, 'r') as f:
                text = f.readlines()
            Content, word_num = merge_clean(text)
            comments_inf_df.loc[i,'comment len'] = word_num
            Content_words_dic={}
            Content_words_dic = content_to_dic(Content, Content_words_dic)
            rule_comment_word_dic = content_to_dic(Content, rule_comment_word_dic)
            bag_of_word_one_list.append(Content_words_dic)
        
#        count_dic=create_dic_df(comments_inf_df, bag_of_word_one_list, rule_comment_word_dic)
        #list of dic
        bag_of_word_one_comment_spe_save_pickle_add = bag_of_words_save_basic_add + "\\separate_" + "rule_type_" + str(rule_type_i) + ".pickle"
        pickle.dump(bag_of_word_one_list, open(bag_of_word_one_comment_spe_save_pickle_add,"wb"))   
        #dic
        bag_of_word_one_total_save_pickle_add = bag_of_words_save_basic_add + "\\total_" + "rule_type_" + str(rule_type_i) + ".pickle"
        pickle.dump(rule_comment_word_dic, open(bag_of_word_one_total_save_pickle_add,"wb"))
        
        pickle.dump(comments_inf_df, open(scrape_result_save_pickle_add,"wb"))
        
#        count_dic_save_pickle_add = bag_of_words_save_basic_add + "\\count_dic_" + "rule_type_" + str(rule_type_i) + ".pickle"
#        pickle.dump(count_dic, open(count_dic_save_pickle_add,"wb"))
        
        





#with open(bag_of_word_one_total_save_pickle_add,"rb") as f:
#    tem=pickle.load(f, encoding='latin1')
##
#with open(bag_of_word_one_comment_spe_save_pickle_add,"rb") as f:
#    tem=pickle.load(f, encoding='latin1')
#
#with open(count_dic_save_pickle_add,"rb") as f:
#    tem=pickle.load(f, encoding='latin1')
















