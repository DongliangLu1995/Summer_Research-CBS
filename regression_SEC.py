# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 14:21:42 2018

@author: DongliangLu
"""

#group regression variable for all possible rule
import pandas as pd
import pickle
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

final_rule_good=[0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]

save_pickle_org_tag=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_org_tag"+".pickle"
with open(save_pickle_org_tag,"rb") as f:
    org_tag_dic=pickle.load(f, encoding='latin1')
org_type_num=max(list(org_tag_dic.values()))
org_tag_dic['Individual']=11


#get x
save_pickle_add_e=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\comments_meeting_SEC.pickle"
with open(save_pickle_add_e,"rb") as f:
    tem_x=pickle.load(f, encoding='latin1')
tem_x['organization type']=tem_x.apply(lambda x: org_tag_dic[x[1]],axis=1)

tem_x=tem_x[tem_x["organization"]!="Individual"]
tem_x['comment_meeting']=tem_x["comment times"]*tem_x["meeting times"]

tem_x['comments percentage']=tem_x.groupby(['rule type num'])['comment times'].transform(lambda x: x/x.sum())
tem_x['meetings percentage']=tem_x.groupby(['rule type num'])['meeting times'].transform(lambda x: x/x.sum())
tem_x['c_m percentage']=tem_x.groupby(['rule type num'])['comment_meeting'].transform(lambda x: x/x.sum())
tem_x=tem_x.fillna(0)
    
save_pickle_citation_percentage=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_citation_percentage"+".pickle"
with open(save_pickle_citation_percentage,"rb") as f:
    citation_percentage=pickle.load(f, encoding='latin1')
citation_per_dic={}

for i in range(org_type_num+1):
    tem_x["org type "+str(i)]=0
    tem_x["org type "+str(i)+" comment times"]=0
    tem_x["org type "+str(i)+" comment times percentage"]=0
    tem_x["org type "+str(i)+" meeting times percentage"]=0
for index, row in tem_x.iterrows():
    organization_type=row['organization type']
#    print(organization_type)
    tem_x.loc[index, "org type "+str(organization_type)]=1
    tem_x.loc[index, "org type "+str(organization_type)+" comment times"]=row['comment times']
    tem_x.loc[index, "org type "+str(organization_type)+" comment times percentage"]=row['comments percentage']
    tem_x.loc[index, "org type "+str(organization_type)+" meeting times percentage"]=row['meetings percentage']
#    row["organization type "+str(organization_type)]=1
#    print(row["organization type "+str(organization_type)])
#rule_type_list=tem_x['rule type num'].unique()
for i in range(len(final_rule_good) ):
    tem_x['rule type index '+str(final_rule_good[i])]=0
#for index, row in tem_x.iterrows():
#    tem_x.loc[index, 'rule type index '+str(int(row['rule type num']))] = 1




for ele in citation_percentage:
    if ele["rule type number"] in final_rule_good:
        citation_per_dic[ele["rule type number"]]={}
        citation_per_dic[ele["rule type number"]]['citation contains org']=ele['citation contains org']
        citation_per_dic[ele["rule type number"]]["total citation"]=ele["total citation"]
        citation_per_dic[ele["rule type number"]]['citation contains org']=ele['citation contains org']
        citation_per_dic[ele["rule type number"]]['citation citing rules']=ele['citation citing rules']
        

data_y=pd.DataFrame()
data_x=pd.DataFrame()
rule_character=[]
for i in final_rule_good:
    data_i_x=tem_x[tem_x["rule type num"] ==i ]
    data_i_x.drop(['rule type'],axis=1,inplace=True)
#    data_i_x=data_i_x[data_i_x["organization"]!="Individual"]
    
    data_x=data_x.append(data_i_x,ignore_index=True)
    
    rule_character.append({})
    
    meeting_times=data_i_x['meeting times'].sum()
    comment_times=data_i_x['comment times'].sum()
    a=data_i_x['meeting times']!=0
    organizations_has_meetings=a.sum()
    b=data_i_x['comment times']!=0
    organizations_has_comments=b.sum()
    c=a*b
    organizations_has_c_and_m=c.sum()
    organizations_has_c_or_m=organizations_has_meetings+organizations_has_comments-organizations_has_c_and_m
    total_citation=citation_per_dic[i]["total citation"]
    citation_citing_rule=citation_per_dic[i]['citation citing rules']
    citation_contains_org=citation_per_dic[i]['citation contains org']
    total_citing_citation=citation_citing_rule+citation_contains_org
#    if total_citation!=0:
#        citation_per=citation_contains_org / total_citation
#    else:
#        citation_per=0
    if total_citing_citation!=0:
        citation_per=citation_contains_org / total_citing_citation
    else:
        citation_per=0
    
    rule_character[-1]["rule type num"]=i
    rule_character[-1]["meeting times"]=meeting_times
    rule_character[-1]["comment times"]=comment_times
    rule_character[-1]["organizations has meetings"]=organizations_has_meetings
    rule_character[-1]["organizations has comments"]=organizations_has_comments
    rule_character[-1]["organizations_has_c_or_m"]=organizations_has_c_or_m
    rule_character[-1]["organizations_has_c_and_m"]=organizations_has_c_and_m
    rule_character[-1]["total citation"]=total_citation
    rule_character[-1]['citation citing rules']=citation_contains_org
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
data_y['citation percentage']=data_y.groupby(['rule type num'])['citation'].transform(lambda x: x/x.sum())
data_rule_character=pd.DataFrame(rule_character)


     
data_reg=data_x.merge(data_y, how="left", on=['organization', 'rule type num'])
data_reg=data_reg.fillna(0)
#data_reg=data_reg[data_reg["organization"]!="Individual"]

for index, row in data_reg.iterrows():
    data_reg.loc[index, 'rule type index '+str(int(row['rule type num']))] = 1

print("total orgs has connections and has citations for all 16 rule")
print(len(data_reg[data_reg["citation"]!=0]))


top_10_comment=pd.DataFrame(data_reg.groupby('organization')['comment times'].sum()).sort_values(by=['comment times'], ascending=False)[:10]
top_10_meeting=pd.DataFrame(data_reg.groupby('organization')['meeting times'].sum()).sort_values(by=['meeting times'], ascending=False)[:10]
top_10_citation=pd.DataFrame(data_reg.groupby('organization')['citation'].sum()).sort_values(by=['citation'], ascending=False)[:10]

volcker_reg=data_reg[data_reg["rule type num"]==10]

data_reg.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_regression"+".csv")
volcker_reg.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_regression_v"+".csv")
data_rule_character.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_rule_character"+".csv")

x=range(8)
plt.bar(x,top_10_comment.values[:8])
#xt=['SIFMA', 'ISDA', 'General Counsel', 'FSR', 'ABA', 'Morgan Stanley',
#       'MFA', 'Chamber', 'ASF', 'CFA']
xt=['SIFMA', 'ISDA', 'General Counsel', 'FSR', 'ABA', 'Morgan Stanley',
       'MFA', 'Chamber']
plt.xticks(x,xt)
plt.xlabel('organization')
plt.ylabel('comment times')
plt.title('top 8 organizations having most comments')







plt.bar(x,top_10_meeting.values[:8])
plt.xticks(x,['SIFMA','Goldman Sachs', 'Morgan Stanley', 'ISDA',
       'AFR', 'Barclays', 'MFA', 'Nomura'][:8])
plt.xlabel('organization')
plt.ylabel('meeting times')
plt.title('top 8 organizations having most meetings')

plt.bar(x,top_10_citation.values[:8])
plt.xticks(x,['SIFMA', 'Goldman Sachs', 'Occupy the SEC', 'IIB', 'Credit Suisse',
       'ABA', 'Bank of America', 'ASF', 'ISDA', 'JP Morgan'])
plt.xlabel('organization')
plt.ylabel('citation times')
plt.title('top 8 organizations having most citations')

y=top_10_citation.values[:8]
plt.barh(x,y)
plt.yticks(y,['SIFMA', 'Goldman Sachs', 'Occupy the SEC', 'IIB', 'Credit Suisse',
       'ABA', 'Bank of America', 'ASF', 'ISDA', 'JP Morgan'])
plt.xlabel('organization')
plt.ylabel('citation times')
plt.title('top 8 organizations having most citations')





objects = ['SIFMA', 'Goldman Sachs', 'Occupy the SEC', 'IIB', 'Credit Suisse',
       'ABA', 'Bank of America', 'ASF', 'ISDA', 'JP Morgan']
y_pos = np.arange(len(objects))[::-1]
performance = top_10_citation.values
 
plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Citation')
plt.title('top 10 organizations having most citations')




#
s=data_rule_character['citation percentage']+0.00001
s=s/s.max()
s=s*200
plt.scatter(data_rule_character['comment times'], data_rule_character['meeting times'],s=s,c=data_rule_character['rule type num'])
plt.xlabel("total comment times from organizations")
plt.ylabel("total meeting times")
plt.title("citation with organization percentage")
#
#
plt.scatter(data_rule_character['organizations has comments'], data_rule_character['organizations has meetings'],s=s,c=data_rule_character['rule type num'])
plt.xlabel('organizations has comments')
plt.ylabel("total meeting times")
plt.title("citation with organization percentage")
#
#
#
plt.scatter(data_rule_character['comment times'], data_rule_character['organizations has meetings'],s=s,c=data_rule_character['rule type num'])
plt.xlabel("total comment times")
plt.ylabel('organizations has meetings')
plt.title("citation with organization percentage")
#
#
s2=data_rule_character['citation contains org']+0.00001
s2=s2/s2.max()
s2=s2*500
plt.scatter(data_rule_character['comment times'], data_rule_character['meeting times'],s=s2,c=data_rule_character['rule type num'])
plt.xlabel('comment times')
plt.ylabel("meeting times")
plt.title("citation contains org")
#
#
#
#
#
plt.scatter(data_rule_character['citation contains org'],data_rule_character['citation percentage'])
plt.xlabel("citation contains org")
plt.ylabel("citation percentage")
#
##%pylab inline
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data_reg['meeting times'], data_reg['comment times'], data_reg['citation'], c=data_reg['rule type num'], marker='o')
fig.show()
#
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(volcker_reg['meeting times'], volcker_reg['comment times'], volcker_reg['citation'], c=volcker_reg['rule type num'], marker='o')
fig.show()
#
#
with open(save_pickle_add_e,"rb") as f:
    statis_data=pickle.load(f, encoding='latin1')
statis_data['organization type']=statis_data.apply(lambda x: org_tag_dic[x[1]],axis=1)
comment_org_type=statis_data.groupby(['organization type'])['comment times'].sum()
meeting_org_type=statis_data.groupby(['organization type'])['meeting times'].sum()
citation_org_type=data_reg.groupby(['organization type'])['citation'].sum()

label_dic={0:"congress",
           1:"",
           2:"big financial inst.",
           3:"other financial inst.",
           4:"real estate",
           5:"insurance",
           6:"law/lobby",
           7:"other ass.n",
           8:"other",
           9:"financial ass.n",
           10:"university",
           11:"individual",
        }
#
label=[label_dic[i] for i in label_dic.keys() if i!=4]

plt.pie(list(comment_org_type),labels=label)
plt.pie(list(comment_org_type),labels=label,autopct='%1.1f%%')
total_comments=statis_data['comment times'].sum()
plt.title("comments from different organizations(%4.0d)"%total_comments)
#
#
label_dic={0:"congress",
           1:"gov",
           2:"big financial inst.",
           3:"other financial inst.",
           4:"real estate",
           5:"insurance",
           6:"law/lobby",
           7:"other ass.n",
           8:"other",
           9:"financial ass.n",
           10:"university",
           11:"",
        }
label=[label_dic[i] for i in label_dic.keys() if i!=4 and i!=11]
plt.pie(list(meeting_org_type)[:-1],labels=label,autopct='%1.1f%%')
total_meetings=statis_data['meeting times'].sum()
plt.title("meetings from different organizations(%4.0d)"%total_meetings)
#
label2=[label_dic[i] for i in label_dic.keys() if i!=4 and i!=11]
plt.pie(list(citation_org_type),labels=label2,autopct='%1.1f%%')
total_citations=citation_org_type.sum()
plt.title("citations from different organizations(%4.0d)"%total_citations)





y_label = ["big financial inst.","other financial inst.","insurance","law/lobby","other ass.n","other","financial ass.n","university","individual"]
objects = y_label
y_pos = np.arange(len(objects))[::-1]
performance = [125.0, 126.0, 33.0, 76.0, 262.0, 69.0, 424.0, 16.0, 4214.0]
 
ax = plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Comment Times')
plt.title('Comment Times for Different Organization Type')

rects = ax.patches
labels = ["label%d" % i for i in np.arange(len(rects))]

for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label,
            ha='center', va='bottom')






frequencies = np.log(np.array([125.0, 126.0, 33.0, 76.0, 262.0, 69.0, 424.0, 16.0, 4214.0][::-1]))
frequencies = [int(i) for i in frequencies]
freq_series = pd.Series(frequencies)
y_label=['big financial inst.',
 'other financial inst.',
 'insurance',
 'law/lobby',
 'other ass.n',
 'other',
 'financial ass.n',
 'university',
 'individual']
y_labels = y_label[::-1]

# Plot the figure.
plt.figure(figsize=(12, 8))
ax = freq_series.plot(kind='barh')
ax.set_title('Comment Times for Different Organization Type')
ax.set_xlabel('Comment Times')
ax.set_yticklabels(y_labels, size=9.5,fontweight='bold')
ax.set_xlim(0, 4250) # expand xlim to make labels easier to read

rects = ax.patches

# For each bar: Place a label
for rect in rects:
    # Get X and Y placement of label from rect.
    x_value = rect.get_width()
    y_value = rect.get_y() + rect.get_height() / 2

    # Number of points between bar and label. Change to your liking.
    space = 5
    # Vertical alignment for positive values
    ha = 'left'

    # If value of bar is negative: Place label left of bar
    if x_value < 0:
        # Invert space to place label to the left
        space *= -1
        # Horizontally align label at right
        ha = 'right'

    # Use X value as label and format number with one decimal place
    label = "{:.1f}".format(x_value)

    # Create annotation
    plt.annotate(
        label,                      # Use `label` as label
        (x_value, y_value),         # Place label at end of the bar
        xytext=(space, 0),          # Horizontally shift label by `space`
        textcoords="offset points", # Interpret `xytext` as offset in points
        va='center',                # Vertically center label
        ha=ha)                      # Horizontally align label differently for
                                    # positive and negative values.

plt.savefig(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\final presentation"+"\\comments")




frequencies = top_10_citation.values
frequencies = [int(i) for i in frequencies][::-1]

freq_series = pd.Series(frequencies)

y_labels = ['SIFMA', 'Goldman Sachs', 'Occupy the SEC', 'IIB', 'Credit Suisse','ABA', 'Bank of America', 'ASF', 'ISDA', 'JP Morgan'][::-1]

# Plot the figure.
plt.figure(figsize=(12, 8))
ax = freq_series.plot(kind='barh')
ax.set_title('Top 10 Organizations being Cited')
ax.set_xlabel('Citation Times')
ax.set_yticklabels(y_labels,size = 11,fontweight = 'bold')
#ax.set_xlim(-40, 300) # expand xlim to make labels easier to read

rects = ax.patches

# For each bar: Place a label
for rect in rects:
    # Get X and Y placement of label from rect.
    x_value = rect.get_width()
    y_value = rect.get_y() + rect.get_height() / 2

    # Number of points between bar and label. Change to your liking.
    space = 5
    # Vertical alignment for positive values
    ha = 'left'

    # If value of bar is negative: Place label left of bar
    if x_value < 0:
        # Invert space to place label to the left
        space *= -1
        # Horizontally align label at right
        ha = 'right'

    # Use X value as label and format number with one decimal place
    label = "{:.1f}".format(x_value)

    # Create annotation
    plt.annotate(
        label,                      # Use `label` as label
        (x_value, y_value),         # Place label at end of the bar
        xytext=(space, 0),          # Horizontally shift label by `space`
        textcoords="offset points", # Interpret `xytext` as offset in points
        va='center',                # Vertically center label
        ha=ha)                      # Horizontally align label differently for
                                    # positive and negative values.



plt.savefig(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\final presentation"+"\\citation.png")











