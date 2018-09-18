# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 16:24:22 2018

@author: DongliangLu
"""

#match organization to citation location
import pickle
import numpy as np
import pandas as pd





citation_location_basic_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\citation_location"


final_rule_good = [0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]
final_rule_good = [2]
for rule_type_i in final_rule_good: 

    location_save_pickle_add_i = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_citation_location_"+str(rule_type_i)+".pickle"
    citation_location_save_add = citation_location_basic_add + "\\rule_citation_location_dic_"+str(rule_type_i) +".pickle"
    
    with open(location_save_pickle_add_i,"rb") as f:
        tem=pickle.load(f)
    org_citation_location = tem
    
    with open(citation_location_save_add,"rb") as f:
        tem=pickle.load(f)  
    citation_location = tem
    
org_citation_location['ISDA']
citation_location['140']

















