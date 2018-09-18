# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 11:18:44 2018

@author: DongliangLu
"""

#merge similarity citation contains individual
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
new_df_individual = pd.DataFrame()
for rule_type_i in final_rule_good:

    similarity_save_add = similarity_save_basic_add +"\\similarity_agg_"+"One"+"_" + str(rule_type_i) +".pickle"
    with open(similarity_save_add,"rb") as f:
        tem=pickle.load(f, encoding='latin1')
    comments_inf = tem
    comments_inf_needed = comments_inf[inf_need_list]
    comments_inf_needed_individual = comments_inf_needed[comments_inf_needed['identify org'] == "Individual" ]
    comments_inf_needed = comments_inf_needed[ comments_inf_needed['identify org'] != "Individual" ]
    
    
    total_comment_len = comments_inf_needed.groupby(['identify org'])['comment len'].sum()
    comment_similarity = comments_inf_needed.groupby(['identify org'])[['tfidf similarity','set similarity','count similarity','pca set similarity', 
                                                    'pca count similarity', 'pca tfidf similarity',]].mean()
    comment_distance = comments_inf_needed.groupby(['identify org'])[['tfidf distance','set distance','count distance',
                                                  'pca count distance', 'pca set distance', 'pca tfidf distance']].mean()
    
    total_comment_len_individual = comments_inf_needed_individual['comment len']
    comment_similarity_individual = comments_inf_needed_individual[['tfidf similarity','set similarity','count similarity','pca set similarity', 
                                                    'pca count similarity', 'pca tfidf similarity',]]
    comment_distance_individual = comments_inf_needed_individual[['tfidf distance','set distance','count distance',
                                                  'pca count distance', 'pca set distance', 'pca tfidf distance']]
    
    
    
    
    merge_1=pd.concat([total_comment_len,comment_similarity,comment_distance], axis=1)
    merge_1["organization"] = merge_1.index
    merge_1['rule type'] = rule_type_i 
    merge_1.reset_index(inplace=True)
    
    merge_2 = pd.concat([total_comment_len_individual, comment_similarity_individual, comment_distance_individual], axis=1)
    merge_2['rule type'] = rule_type_i
    merge_2["organization"] = 'Individual'
    merge_2.reset_index(inplace=True)
    
    
    new_df = new_df.append(merge_1)
    new_df_individual = new_df_individual.append(merge_2)
    
new_df = new_df[['organization','tfidf similarity','set similarity','count similarity',
                 'pca set similarity', 'pca count similarity', 'pca tfidf similarity',
                 'count distance', 'set distance', 'tfidf distance',
                 'pca count distance', 'pca set distance', 'pca tfidf distance',
                 "rule type",'comment len']]


new_df = new_df.rename(columns={'rule type': 'rule type num'})
#new_df['count similarity transformed'] = -np.log(1 - new_df['count similarity']**2)
#new_df['set similarity transformed'] = -np.log(1 - new_df['set similarity']**2)
#new_df['tfidf similarity transformed'] = -np.log(1 - new_df['tfidf similarity']**2)
#new_df['pca count similarity transformed'] = -np.log(1 - new_df['pca count similarity']**2)
#new_df['pca set similarity transformed'] = -np.log(1 - new_df['pca set similarity']**2)
#new_df['pca tfidf similarity transformed'] = -np.log(1 - new_df['pca tfidf similarity']**2)

new_df['count similarity transformed'] = -np.log(1 - new_df['count similarity'])
new_df['set similarity transformed'] = -np.log(1 - new_df['set similarity'])
new_df['tfidf similarity transformed'] = -np.log(1 - new_df['tfidf similarity'])
new_df['pca count similarity transformed'] = -np.log(1 - new_df['pca count similarity'])
new_df['pca set similarity transformed'] = -np.log(1 - new_df['pca set similarity'])
new_df['pca tfidf similarity transformed'] = -np.log(1 - new_df['pca tfidf similarity'])





new_df.fillna(0)


new_df_individual = new_df_individual[['organization','tfidf similarity','set similarity','count similarity',
                 'pca set similarity', 'pca count similarity', 'pca tfidf similarity',
                 'count distance', 'set distance', 'tfidf distance',
                 'pca count distance', 'pca set distance', 'pca tfidf distance',
                 "rule type",'comment len']]
new_df_individual = new_df_individual.rename(columns={'rule type': 'rule type num'})
#new_df_individual['count similarity transformed'] = -np.log(1 - new_df_individual['count similarity']**2)
#new_df_individual['set similarity transformed'] = -np.log(1 - new_df_individual['set similarity']**2)
#new_df_individual['tfidf similarity transformed'] = -np.log(1 - new_df_individual['tfidf similarity']**2)
#new_df_individual['pca count similarity transformed'] = -np.log(1 - new_df_individual['pca count similarity']**2)
#new_df_individual['pca set similarity transformed'] = -np.log(1 - new_df_individual['pca set similarity']**2)
#new_df_individual['pca tfidf similarity transformed'] = -np.log(1 - new_df_individual['pca tfidf similarity']**2)


new_df_individual['count similarity transformed'] = -np.log(1 - new_df_individual['count similarity'])
new_df_individual['set similarity transformed'] = -np.log(1 - new_df_individual['set similarity'])
new_df_individual['tfidf similarity transformed'] = -np.log(1 - new_df_individual['tfidf similarity'])
new_df_individual['pca count similarity transformed'] = -np.log(1 - new_df_individual['pca count similarity'])
new_df_individual['pca set similarity transformed'] = -np.log(1 - new_df_individual['pca set similarity'])
new_df_individual['pca tfidf similarity transformed'] = -np.log(1 - new_df_individual['pca tfidf similarity'])




#has some problem on pca set similarity, and all pca transformed similarity

data_reg=citation_df.merge(new_df, how="left", on=['organization', 'rule type num'])
data_reg = data_reg.fillna(0)

#data_reg_individual = data_reg.merge(new_df_individual, how = "outer", on = ['organization', 'rule type num'] )

data_reg_individual = data_reg.append(new_df_individual)

data_reg_individual = data_reg_individual.fillna(value = {"comment times":1,"organization type":11})
data_reg_individual = data_reg_individual.fillna(0)


data_reg_individual.reset_index(inplace=True)


for index, row in data_reg_individual.iterrows():
    organization_type=int(row['organization type'])
#    print(organization_type)
    data_reg_individual.loc[index, "org type "+str(organization_type)]=1
    data_reg_individual.loc[index, "org type "+str(organization_type)+" comment times"]=row['comment times']
    data_reg_individual.loc[index, "org type "+str(organization_type)+" comment times percentage"]=row['comments percentage']
    data_reg_individual.loc[index, "org type "+str(organization_type)+" meeting times percentage"]=row['meetings percentage']

    rule_type = int(row['rule type num'])
    data_reg_individual.loc[index, "rule type index "+str(rule_type)] = 1

data_reg_individual = data_reg_individual.fillna(0)

#data_reg_individual['individual or not'] = 1
#data_reg_individual['individual ind'] = 0
#data_reg_individual['non-individual ind'] = 0
#for index, row in data_reg_individual.iterrows():
#    org = 


#data_reg_individual.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\new_reg_individual_agg.csv")


df_for_see = data_reg_individual[['rule type num', 'comment times', 'meeting times',
                                  'set similarity', 'pca set distance','comment len']]

df_for_see_no_zero = df_for_see[df_for_see['comment times']!=0]

t=data_reg_individual[data_reg_individual['organization']!='Individual']
t1=t[t['comment len']!=0]
t1[['citation']]
t2=t1[['citation','set similarity','set similarity transformed','tfidf similarity']].values





























