# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 11:39:19 2018

@author: DongliangLu
"""

import pandas as pd
import numpy as np
import pickle




scrape_result_basic_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\scrape_comment_result_SEC"
bag_of_words_save_basic_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\bag_of_words\one"

final_rule_good=[0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]

data_Y_in = pd.DataFrame()
data_X_in = []
for rule_type_i in final_rule_good:
    scrape_result_add = scrape_result_basic_add + "\\" +str(rule_type_i) +".pickle"
    with open(scrape_result_add,"rb") as f:
        tem=pickle.load(f, encoding='latin1')
    comments_df=tem
    
    bag_of_words_separate_add = bag_of_words_save_basic_add + "\\" +"\\separate_rule_type_" +str(rule_type_i) +".pickle"
    with open(bag_of_words_separate_add,"rb") as f:
        tem=pickle.load(f, encoding='latin1')
    comments_sep_dic=tem
    
    data_Y_in = data_Y_in.append(comments_df)
    data_X_in.extend(comments_sep_dic)
data_Y_in.reset_index(inplace=True)
have_comment = data_Y_in['comment len']!=0

data_X_in = pd.DataFrame(data_X_in)
data_X_in = data_X_in.fillna(0)

Y=data_Y_in[have_comment]['rule type']
X=data_X_in[have_comment].values


ML_data_save_basic_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\ML"
Y_save_add = ML_data_save_basic_add + "\\Y.pickle"
X_save_add = ML_data_save_basic_add + "\\X.pickle"

pickle.dump(X, open(X_save_add,"wb"))
pickle.dump(Y, open(Y_save_add,"wb"))


























