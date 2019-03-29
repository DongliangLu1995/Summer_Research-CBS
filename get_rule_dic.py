# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 00:27:58 2019

@author: DongliangLu
"""

#cluster the final rule
import numpy as np
import pandas as pd
import re

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
        S+=line.strip()
        S+=" "
    for p in punct:
        S=S.replace(p,"")
    S=" ".join([ porter_stemmer.stem(i) for i in S.lower().split() if i not in stop])
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
#def create_dic_df(separate_dic, total_dic):
#    new_index=np.arange(len(separate_dic))
#    new_columns=total_dic.keys()
#    new_df=pd.DataFrame(index=new_index, columns=new_columns)
#    new_df=new_df.fillna(0)
#    
#    for comment_i in range(len(separate_dic)):
#        comment_dic=separate_dic[comment_i]
#        for word_j in comment_dic.keys():
#            new_df.loc[comment_i, word_j ]=comment_dic[word_j]
#
#    return new_df



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


with open(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw"+r"\scrape_SEC.pickle","rb") as f:
    tem=pickle.load(f, encoding='latin1')
scrape_SEC = tem  
scrape_SEC['rule type']=0
for i in range(len(scrape_SEC)):
    scrape_SEC.loc[i,'rule type'] = i
final_rule_good_df = scrape_SEC[scrape_SEC['good final rule or not']==1]

final_rule_good = [int(r) for r in list(final_rule_good_df['rule type'])]


#first_time = False


#final_rule_good=[0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]
#final_rule_good=[2]

final_rule_basic_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw\final_rule"
bag_of_words_save_basic_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw\final_rule"
citation_location_basic_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw\final_rule"

#final_rule_good = final_rule_good[:2] 
rule_corpus_dic={}
rule_dic_total = []
for rule_type_i in final_rule_good:
    print("dealing with rule %i"%rule_type_i)
    
    
    
    final_rule_add = final_rule_basic_add + "\\" + str(rule_type_i) + "\\" + str(rule_type_i) +".pdf"
#    if first_time:
#        not_usable=convery_pdf_to_txt(final_rule_add)
    final_rule_txt_add = final_rule_add.replace(".pdf", ".txt")
    bag_of_word_final_rule={}
    with open(final_rule_txt_add, 'r') as f:
        text = f.readlines()
    
    Content = merge_clean(text)
    Content_words_dic={}
    Content_words_dic = content_to_dic(Content, Content_words_dic)
    rule_corpus_dic = content_to_dic(Content, rule_corpus_dic)
    rule_dic_total.append(Content_words_dic)
    
    rule_bag_of_word_save_add = bag_of_words_save_basic_add + "\\" + str(rule_type_i) + "\\" + str(rule_type_i) +"_unigram.pickle"
    pickle.dump(Content_words_dic,open(rule_bag_of_word_save_add,"wb"))

#    merged_text = merge_lines(text)
#    citation_dic = find_citation_location(merged_text)
#    
#    citation_location_save_add = citation_location_basic_add + "\\rule_citation_location_dic_"+str(rule_type_i) +".pickle"
#    pickle.dump(citation_dic,open(citation_location_save_add,"wb"))

rule_corpus_save_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw" + "\\rule_corpus_unigram.pickle"
pickle.dump(rule_corpus_dic,open(rule_corpus_save_add,"wb"))

rule_unigram_df = pd.DataFrame(rule_dic_total)
rule_unigram_df  = rule_unigram_df.fillna(0)
rule_unigram_df['rule type'] = final_rule_good
#rule_unigram_df = create_dic_df( rule_dic_total, rule_corpus_dic )
rule_unigram_df_save_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw" + "\\rule_df_unigram.pickle"
pickle.dump(rule_unigram_df,open(rule_unigram_df_save_add,"wb"))




#for i in text:
#    if porter_stemmer.stem(i) == 'stresses':
#        print(i)

































