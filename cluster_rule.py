# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 00:27:58 2019

@author: DongliangLu
"""

#cluster the final rule
import numpy as np
import pandas as pd
import re
from collections import Counter
import os
import pickle

from sklearn.cluster import KMeans

with open(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw"+r"\scrape_SEC.pickle","rb") as f:
    tem=pickle.load(f, encoding='latin1')
scrape_SEC = tem  
scrape_SEC['rule type']=0
for i in range(len(scrape_SEC)):
    scrape_SEC.loc[i,'rule type'] = i
final_rule_good_df = scrape_SEC[scrape_SEC['good final rule or not']==1]

final_rule_good = [int(r) for r in list(final_rule_good_df['rule type'])]



rule_unigram_df_save_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw" + "\\rule_df_unigram.pickle"
with open(rule_unigram_df_save_add,"rb") as f:
    tem=pickle.load(f, encoding='latin1')
rule_unigram_df = tem

rule_type_list = rule_unigram_df['rule type']
del rule_unigram_df['rule type']

X=np.array( rule_unigram_df)

kmeans_3 = KMeans(n_clusters=3, random_state=0).fit(X)
kmeans_2 = KMeans(n_clusters=2, random_state=0).fit(X)
kmeans_4 = KMeans(n_clusters=4, random_state=0).fit(X)
kmeans_5 = KMeans(n_clusters=5, random_state=0).fit(X)
a3=kmeans_3.labels_
a2=kmeans_2.labels_
a4=kmeans_4.labels_
a5=kmeans_5.labels_
date = scrape_SEC.loc[rule_type_list,'date']
description = scrape_SEC.loc[rule_type_list,'rule name']
cluster={'description':description,'date':date,"center 2":a2,"center 3":a3,"center 4":a4,"center 5":a5}
cluster = pd.DataFrame(cluster)



cluster_save_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\scale_up\raw" + "\\rule_cluster.pickle"
pickle.dump(cluster,open(cluster_save_add,"wb"))

cluster_save_add_csv = cluster_save_add.replace('.pickle','.csv')
cluster.to_csv(cluster_save_add_csv, index = False)






























