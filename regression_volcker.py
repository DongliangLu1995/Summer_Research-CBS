# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 11:51:52 2018

@author: DongliangLu
"""

#group regression variable for volcker rule
import pandas as pd
import pickle


save_pickle_add_v=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_citation"+str(1)+".pickle"
with open(save_pickle_add_v,"rb") as f:
    tem=pickle.load(f, encoding='latin1')

data_y=pd.DataFrame(tem)

save_pickle_add_e=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\comments_meeting_SEC.pickle"
#pickle.dump(df_all, open(save_pickle_add_e,"wb"))
with open(save_pickle_add_e,"rb") as f:
    tem=pickle.load(f, encoding='latin1')
    
data_v_x=tem[tem["rule type num"] ==1 ]
data_v_x=data_v_x.append(tem[tem["rule type num"] ==10 ],ignore_index=True)
data_v_x.drop(['rule type','rule type num'],axis=1,inplace=True)

df_reg_volcker=data_v_x.merge(data_y, how='left',on=['organization'])
df_reg_volcker.drop(['rule type number'],axis=1,inplace=True)
save_pickle_add_regre_v=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\volcker_regression"+".pickle"
#pickle.dump(df_reg_volcker,open(save_pickle_add_regre_v,"wb"))
with open(save_pickle_add_v,"rb") as f:
    tem=pickle.load(f, encoding='latin1')

df_reg_volcker.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\volcker_regression"+".csv")







































