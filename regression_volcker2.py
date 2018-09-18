# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 14:21:42 2018

@author: DongliangLu
"""

#group regression variable for all possible rule
import pandas as pd
import pickle

final_rule_good=[0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]

save_pickle_org_tag=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_org_tag"+".pickle"
with open(save_pickle_org_tag,"rb") as f:
    org_tag_dic=pickle.load(f, encoding='latin1')
org_type_num=max(list(org_tag_dic.values()))


#get x
save_pickle_add_e=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\comments_meeting_SEC.pickle"
with open(save_pickle_add_e,"rb") as f:
    tem_x=pickle.load(f, encoding='latin1')
tem_x['organization type']=tem_x.apply(lambda x: org_tag_dic[x[1]],axis=1)
    
save_pickle_citation_percentage=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_citation_percentage"+".pickle"
with open(save_pickle_citation_percentage,"rb") as f:
    citation_percentage=pickle.load(f, encoding='latin1')
citation_per_dic={}

for i in range(org_type_num+1):
    tem_x["organization type "+str(i)]=0
    tem_x["organization type "+str(i)+" comment times"]=0
for index, row in tem_x.iterrows():
    organization_type=row['organization type']
#    print(orginzation_type)
    tem_x.loc[index, "organization type "+str(organization_type)]=1
    tem_x.loc[index, "organization type "+str(organization_type)+" comment times"]=row['comment times']
#    row["organization type "+str(orginzation_type)]=1
#    print(row["organization type "+str(orginzation_type)])


for ele in citation_percentage:
    if ele["rule type number"] in final_rule_good:
        citation_per_dic[ele["rule type number"]]={}
        citation_per_dic[ele["rule type number"]]['citation contains org']=ele['citation contains org']
        citation_per_dic[ele["rule type number"]]["total citation"]=ele["total citation"]
        
        
#        if ele["total citation"]!=0:
#            citation_per_dic[ele["rule type number"]]=ele['citation contains org']/ele["total citation"]
#        else:
#            citation_per_dic[ele["rule type number"]]=0
        


data_y=pd.DataFrame()
data_x=pd.DataFrame()
rule_character=[]
for i in final_rule_good:
    data_i_x=tem_x[tem_x["rule type num"] ==i ]
    data_i_x.drop(['rule type'],axis=1,inplace=True)
    data_i_x=data_i_x[data_i_x["organization"]!="Individual"]
    
    
    data_x=data_x.append(data_i_x,ignore_index=True)
    
    rule_character.append({})
    
    meeting_times=data_i_x['meeting times'].sum()
    comment_times=data_i_x['comment times'].sum()
    a=data_i_x['meeting times']!=0
    orginzations_has_meetings=a.sum()
    b=data_i_x['comment times']!=0
    orginzations_has_comments=b.sum()
    c=a*b
    orginzations_has_c_and_m=c.sum()
    orginzations_has_c_or_m=orginzations_has_meetings+orginzations_has_comments-orginzations_has_c_and_m
    total_citation=citation_per_dic[i]["total citation"]
    citation_contains_org=citation_per_dic[i]['citation contains org']
    if total_citation!=0:
        citation_per=citation_contains_org / total_citation
    else:
        citation_per=0
    
    rule_character[-1]["rule type num"]=i
    rule_character[-1]["meeting times"]=meeting_times
    rule_character[-1]["comment times"]=comment_times
    rule_character[-1]["orginzations has meetings"]=orginzations_has_meetings
    rule_character[-1]["orginzations has comments"]=orginzations_has_comments
    rule_character[-1]["orginzations_has_c_or_m"]=orginzations_has_c_or_m
    rule_character[-1]["orginzations_has_c_and_m"]=orginzations_has_c_and_m
    rule_character[-1]["total citation"]=total_citation
    rule_character[-1]["citation contains org"]=citation_contains_org
    rule_character[-1]["citation percentage"]=citation_per
    
    
    
    save_pickle_add_i=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_citation"+str(i)+".pickle"
    with open(save_pickle_add_i,"rb") as f:
        tem=pickle.load(f, encoding='latin1')
    tem=pd.DataFrame(tem)
    print("rule num: "+str(i))
    print("organizations ever have had meetings or comments on this rule: "+str(len(data_i_x)))
    print("citation containing organizations percentage: "+str(citation_per))
    print("none zero citation org: "+ str(len(tem[tem["citation"]!=0])))
    
    rule_character[-1]["none zero citation org"]=len(tem[tem["citation"]!=0])
    
    data_y=data_y.append(tem,ignore_index=True)
data_y=data_y.rename(columns={'rule type number':'rule type num'})
data_rule_character=pd.DataFrame(rule_character)

    
     
data_reg=data_x.merge(data_y, how="left", on=['organization', 'rule type num'])
data_reg=data_reg.fillna(0)
data_reg=data_reg[data_reg["organization"]!="Individual"]


print("total orgs has connections and has citations for all 16 rule")
print(len(data_reg[data_reg["citation"]!=0]))

#data_reg.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_regression"+".csv")

data_reg=data_reg[data_reg['citation']<=60]
data_reg=data_reg[data_reg['citation']>0]

volcker_reg=data_reg[data_reg["rule type num"]==10]
volcker_reg.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_regression_v2"+".csv")
#data_rule_character.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_rule_character"+".csv")



#save_pickle_add_regre=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_regression"+".pickle"
#pickle.dump(save_pickle_add_regre,open(save_pickle_add_regre,"wb"))
#with open(save_pickle_add_regre,"rb") as f:
#    tem=pickle.load(f, encoding='latin1')



#save_pickle_add_regre_x=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_regression_x"+".pickle"
#pickle.dump(data_x,open(save_pickle_add_regre_x,"wb"))
#with open(save_pickle_add_regre_x,"rb") as f:
#    tem=pickle.load(f, encoding='latin1')
#
#data_x.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_regression_x"+".csv")
#
#


#meeting_times=data_i_x['meeting times'].sum()
#comment_times=data_i_x['comment times'].sum()
#a=data_i_x['meeting times']!=0
#orginzations_has_meetings=a.sum()
#b=data_i_x['comment times']!=0
#orginzations_has_comments=b.sum()
#c=a*b
#orginzations_has_c_and_m=c.sum()
#orginzations_has_c_or_m=orginzations_has_meetings+orginzations_has_comments-orginzations_has_c_and_m
#total_citation=ele["total citation"]
#citation_contains_org=ele['citation contains org']
#if total_citation!=0:
#    citation_per=citation_contains_org / total_citation
#else:
#    citation_per=0








