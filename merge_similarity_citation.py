# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 15:14:55 2018

@author: DongliangLu
"""

#merge similarity citation
import pandas as pd
import numpy as np
import pickle



similarity_save_basic_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\comments_similarity\One"

old_data_save_basic_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"
old_data_save_add = old_data_save_basic_add + "\\SEC_regression.csv"
citation_df=pd.read_csv(old_data_save_add, index_col=0)



final_rule_good = [0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]
#rule_type_i=0
inf_need_list = ['rule type','identify org','comment len','set similarity', 'count similarity', 'tfidf similarity',
       'pca set similarity', 'pca count similarity', 'pca tfidf similarity',
       'count distance', 'set distance', 'tfidf distance',
       'pca count distance', 'pca set distance', 'pca tfidf distance']
new_df=pd.DataFrame()
for rule_type_i in final_rule_good:

    similarity_save_add = similarity_save_basic_add +"\\similarity_"+"One"+"_" + str(rule_type_i) +".pickle"
    with open(similarity_save_add,"rb") as f:
        tem=pickle.load(f, encoding='latin1')
    comments_inf = tem
    comments_inf_needed = comments_inf[inf_need_list]
    comments_inf_needed = comments_inf_needed[ comments_inf_needed['identify org'] != "Individual" ]
    
    total_comment_len = comments_inf_needed.groupby(['identify org'])['comment len'].sum()
    comment_similarity = comments_inf_needed.groupby(['identify org'])[['tfidf similarity','set similarity','count similarity','pca set similarity', 
                                                    'pca count similarity', 'pca tfidf similarity',]].mean()
    comment_distance = comments_inf_needed.groupby(['identify org'])[['tfidf distance','set distance','count distance',
                                                  'pca count distance', 'pca set distance', 'pca tfidf distance']].mean()
    
    
    
    merge_1=pd.concat([total_comment_len,comment_similarity,comment_distance], axis=1)
    merge_1["organization"] = merge_1.index
    merge_1['rule type'] = rule_type_i 
    merge_1.reset_index(inplace=True)
    
    new_df = new_df.append(merge_1)
new_df = new_df[['organization','tfidf similarity','set similarity','count similarity',
                 'pca set similarity', 'pca count similarity', 'pca tfidf similarity',
                 'count distance', 'set distance', 'tfidf distance',
                 'pca count distance', 'pca set distance', 'pca tfidf distance',
                 "rule type"]]
new_df = new_df.rename(columns={'rule type': 'rule type num'})
new_df['count similarity transformed'] = -np.log(1 - new_df['count similarity']**2)
new_df['set similarity transformed'] = -np.log(1 - new_df['set similarity']**2)
new_df['tfidf similarity transformed'] = -np.log(1 - new_df['tfidf similarity']**2)
new_df['pca count similarity transformed'] = -np.log(1 - new_df['pca count similarity']**2)
new_df['pca set similarity transformed'] = -np.log(1 - new_df['pca set similarity']**2)
new_df['pca tfidf similarity transformed'] = -np.log(1 - new_df['pca tfidf similarity']**2)

new_df.fillna(0)

#has some problem on pca set similarity, and all pca transformed similarity

data_reg=citation_df.merge(new_df, how="left", on=['organization', 'rule type num'])
data_reg = data_reg.fillna(0)
data_reg.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\new_reg.csv")





































