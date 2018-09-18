# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 14:02:18 2018

@author: DongliangLu
"""

#create regression variables

import pandas as pd
import re
import pickle
import numpy as np

def one_hot(x):
    l=np.max(x)+1
    z=np.zeros((len(x),l))
    z[np.arange(len(x)),x]=1
    return z



save_pickle_add2=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_meeting_small_rule.pickle"
with open(save_pickle_add2,"rb") as f:
    tem=pickle.load(f, encoding='latin1')
    
SEC_meeting=tem

save_pickle_add0=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_rule_dic.pickle"
with open(save_pickle_add0,"rb") as f:
    tem=pickle.load(f, encoding='latin1')


SEC_rule_type_dic=tem

SEC_meeting["rule number"]=0
for i in range(len(SEC_meeting)):
    SEC_meeting.loc[i,"rule number"]=SEC_rule_type_dic[SEC_meeting.loc[i,"rule type"]]
   
    
    
    
X_regression=SEC_meeting
X_regression["comments"]=np.random.randint(5,size=[len(SEC_meeting),1])
X_regression["citations"]=np.random.randint(2,size=[len(SEC_meeting),1])
X_regression.to_csv(save_csv_addx,index=False,header=True)
    

X_regression=np.array(SEC_meeting['meeting times']).reshape(-1,1)
X_comment=np.random.randint(5,size=(len(SEC_meeting),)).reshape(-1,1)

X=one_hot(np.array(SEC_meeting['rule number']))
X=X[:,:-1]
X_regression=np.hstack([X_regression,X_comment])
X_regression=np.hstack([X_regression,X])

Y_regression=np.random.randint(10,size=(len(SEC_meeting),)).reshape(-1,1)

save_csv_addx=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_X.csv"
X_regression=pd.DataFrame(X_regression)
X_regression.to_csv(save_csv_addx,index=False,header=False)


save_csv_addy=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_Y.csv"
Y_regression=pd.DataFrame(Y_regression)
Y_regression.to_csv(save_csv_addy,index=False,header=False)



result_reg1=np.linalg.lstsq(X_regression, Y_regression)
coefficient_reg1=result_reg1[0]
















