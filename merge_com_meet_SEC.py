# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 09:20:14 2018

@author: DongliangLu
"""

#merge comments and meeting for SEC
import pandas as pd
import pickle


save_pickle_add2=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_meeting_small_rule.pickle"
#pickle.dump(SEC_meeting_all, open(save_pickle_add2,"wb"))
with open(save_pickle_add2,"rb") as f:
    tem=pickle.load(f, encoding='latin1')
dataframe_meeting=tem


save_pickle_add0=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_rule_dic.pickle"
#pickle.dump(rule_type_dic, open(save_pickle_add0,"wb"))
with open(save_pickle_add0,"rb") as f:
    tem=pickle.load(f, encoding='latin1')
rule_dic=tem
dataframe_meeting["rule type number"]=0
dataframe_meeting["rule type number"]=dataframe_meeting.apply(lambda x: rule_dic[x[2]],axis=1)
#for i in range(len(dataframe_meeting)):
#    dataframe_meeting.loc[i,"rule type number"]=rule_dic[dataframe_meeting.loc[i,"rule type"]]


dataframe_comment=pd.DataFrame()
for rule_type_num in range(38):
    save_pickle_add_i=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_comments_rule_"+str(rule_type_num)+".pickle"
    with open(save_pickle_add_i,"rb") as f:
        tem=pickle.load(f, encoding='latin1')
    small_rule=pd.DataFrame(tem)
    dataframe_comment=dataframe_comment.append(small_rule,ignore_index=True)
   
dataframe_comment=dataframe_comment.rename(columns={'meeting times':'comment times'})
    
df_all=dataframe_meeting.merge(dataframe_comment, how='outer',on=['organization','rule type'])

df_all["rule type num"]=df_all.apply(lambda x: x[3] if not pd.isna(x[3]) else x[5], axis=1)
df_all.drop(columns=["rule type number_x","rule type number_y"],axis=1, inplace=True)
df_all=df_all.fillna(0)
df_all.sort_values(by=["rule type num","organization"],inplace=True)
df_all=df_all.reset_index(drop=True)    

df_all_10=df_all[df_all["rule type num"]==10]
df_all_1=df_all[df_all["rule type num"]==1]
df_10_1=df_all_10.merge(df_all_1, how="outer", on=["organization"])
Values={'meeting times_x':0,'comment times_x':0,'meeting times_y':0,'comment times_y':0}
df_10_1=df_10_1.fillna(value=Values)
df_10_1['meeting times']=df_10_1['meeting times_x']+df_10_1['meeting times_y']
df_10_1['comment times']=df_10_1['comment times_x']+df_10_1['comment times_y']
df_10_1["rule type"]=df_10_1["rule type_x"]
df_10_1["rule type num"]=df_10_1["rule type num_x"]
df_10_1=df_10_1[list(df_all.columns)]
df_10_1=df_10_1.fillna(10)

df_all=df_all[df_all["rule type num"]!=10]
df_all=df_all[df_all["rule type num"]!=1]
df_all=df_all.append(df_10_1,ignore_index=True)
df_all.sort_values(by=["rule type num","organization"],inplace=True)
df_all=df_all.reset_index(drop=True) 

df_all.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\comments_meeting_SEC.csv")  
save_pickle_add_e=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\comments_meeting_SEC.pickle"
pickle.dump(df_all, open(save_pickle_add_e,"wb"))
#with open(save_pickle_add_e,"rb") as f:
#    tem=pickle.load(f, encoding='latin1')    
    
    

    

