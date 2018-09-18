# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 12:47:28 2018

@author: DongliangLu
"""

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA



import pickle


#def distance(c1,c2):
#    #c1,c2 is np.array
#    a1=np.sum(c1**2)
#    a2=np.sum(c2**2)
#    if a1!=0 and a2!=0:
#        return np.sum( (c1 - c2)**2 )  / (a1 * a2 )**0.5
#    else:
#        return np.nan


def distance(c1,c2):
    #c1,c2 is np.array
    a1=np.sum(c1**2)
    a2=np.sum(c2**2)
    if a1!=0 and a2!=0:
        return  np.sqrt( 1 - np.sum( c1*c2 )**2  / (a1 * a2 ) )
    else:
        return np.nan



def cal_distance_matrix(comment_feature_array):
    
    r,c = comment_feature_array.shape
    m = np.zeros([r,r])
    for row_i in range(r):
        for col_j in range(row_i, r):
            m[row_i, col_j]=distance(comment_feature_array[row_i],comment_feature_array[col_j])
            m[col_j, row_i] = m[row_i, col_j]
    return m

def fill_nan_with_mean(array):
    #array is one dimension
    inds = np.where(np.isnan(array))
    mean_not_nan = np.nanmean(array)
    array[inds] = mean_not_nan
    return array


def calculate_similarity_count(comment_dic_array,i,j):
    #input should be an array, not a df, and it should be count
#    comment_dic_array=comment_dic.values
    return np.sum(comment_dic_array[i]*comment_dic_array[j]) / np.sqrt(np.sum(comment_dic_array[i]**2))/np.sqrt(np.sum(comment_dic_array[j]**2))
    
def calculate_similarity_set(comment_dic_set_array,i,j):
    #input should be an array, and should be set
#    r,c = comment_dic_array.shape
#    comment_dic_set_array=np.ones([r,c]) * (comment_dic_array != 0)
    return np.sum(comment_dic_set_array[i]*comment_dic_set_array[j]) / np.sqrt(np.sum(comment_dic_set_array[i]))/np.sqrt(np.sum(comment_dic_set_array[j]))
     
def calculate_similarity_tfidf(comment_dic_array,i,j):
    #input should be an array, and should be count
    return np.sum(comment_dic_array[i]*comment_dic_array[j]) / np.sqrt(np.sum(comment_dic_array[i]**2))/np.sqrt(np.sum(comment_dic_array[j]**2))


def cal_similarity_matrix(comment_dic, method):
    comment_dic_array = comment_dic.values
    r,c = comment_dic_array.shape
    m = np.zeros([r,r])
    if method == "count":
        for row_i in range(r):
            for col_j in range(row_i, r):
                m[row_i, col_j]=calculate_similarity_count(comment_dic_array,row_i,col_j)
                m[col_j, row_i] = m[row_i, col_j]
    elif method == "set":
        for row_i in range(r):
            for col_j in range(row_i, r):
                m[row_i, col_j]=calculate_similarity_set(comment_dic_array,row_i,col_j)
                m[col_j, row_i] = m[row_i, col_j]
    elif method == "tfidf":
        for row_i in range(r):
            for col_j in range(row_i, r):
                m[row_i, col_j]=calculate_similarity_tfidf(comment_dic_array,row_i,col_j)
                m[col_j, row_i] = m[row_i, col_j]
    return m

def merge_two_dic(dic1, dic2):
    merge_dic={}
    for key in dic1.keys():
        if key in dic2.keys():
            merge_dic[key] = dic1[key] + dic2[key]
        else:
            merge_dic[key] = dic1[key]
    for key in dic2.keys():
        if key in merge_dic:
            pass
        else:
            merge_dic[key]=dic2[key]
    return merge_dic


scrape_result_basic_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\scrape_comment_result_SEC"
bag_of_words_save_basic_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\bag_of_words\One"
final_rule_basic_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\bag_of_words\Rule\One"
similarity_save_basic_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\comments_similarity\One"


agg=1

final_rule_good=[0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]
#rule_type_i=0
#final_rule_good=[10]
final_rule_good=[0]
final_rule_good=[2]
for rule_type_i in final_rule_good:

    scrape_result_add = scrape_result_basic_add + "\\" +str(rule_type_i) +".pickle"
    with open(scrape_result_add,"rb") as f:
        tem=pickle.load(f, encoding='latin1')
    comments_df=tem
    
    bag_of_words_separate_add = bag_of_words_save_basic_add + "\\" +"\\separate_rule_type_" +str(rule_type_i) +".pickle"
    with open(bag_of_words_separate_add,"rb") as f:
        tem=pickle.load(f, encoding='latin1')
    comments_sep_dic=tem
    
    bag_of_words_total_add = bag_of_words_save_basic_add + "\\" +"\\total_rule_type_" +str(rule_type_i) +".pickle"
    with open(bag_of_words_total_add,"rb") as f:
        tem=pickle.load(f, encoding='latin1')
    comments_total_dic=tem
    
    final_rule_add = final_rule_basic_add + "\\rule_word_dic_" + str(rule_type_i) + ".pickle"
    with open(final_rule_add,"rb") as f:
        tem=pickle.load(f, encoding='latin1')
    final_rule_dic=tem
    
    comments_df['file name txt'] = comments_df['file name'].str.replace(".pdf",".txt")
    comments_df['set similarity'] = 0
    comments_df['count similarity'] = 0
    comments_df['tfidf similarity'] = 0
    comments_df['pca set similarity'] = 0
    comments_df['pca count similarity'] = 0
    comments_df['pca tfidf similarity'] = 0
    
    
    #calculate_similarity_2(comment_dic,0,3)
    comments_sep_dic_df = pd.DataFrame(comments_sep_dic)
    comments_sep_dic_df = comments_sep_dic_df.fillna(0)
#    similarity_matrix = cal_similarity_matrix(comments_sep_dic_df, "count")
    
    
    rule_corpus = merge_two_dic(comments_total_dic, final_rule_dic)
    bag_comment_and_rule = comments_sep_dic+[final_rule_dic]
    bag_comment_and_rule_df = pd.DataFrame(bag_comment_and_rule)
    bag_comment_and_rule_df = bag_comment_and_rule_df.fillna(0)
    bag_comment_and_rule_array = bag_comment_and_rule_df.values
    
    bag_comment_and_rule_set_array = np.ones(bag_comment_and_rule_array.shape) * (bag_comment_and_rule_array!=0)
    
    bag_comment_and_rule_tfidf = np.sum(bag_comment_and_rule_set_array, axis = 0)
    bag_comment_and_rule_tfidf = np.log( (1+bag_comment_and_rule_set_array.shape[0] ) /(1 + bag_comment_and_rule_tfidf) )+1
    bag_comment_and_rule_tfidf_array = bag_comment_and_rule_array * bag_comment_and_rule_tfidf 
    
    
    pca = PCA(0.95)
    pca.fit(bag_comment_and_rule_array[:-1])
    bag_comment_and_rule_array_pca = pca.transform(bag_comment_and_rule_array)
    
    pca = PCA(0.95)
    pca.fit(bag_comment_and_rule_set_array[:-1])
    bag_comment_and_rule_set_array_pca = pca.transform(bag_comment_and_rule_set_array)
    
    pca = PCA(0.95)
    pca.fit(bag_comment_and_rule_tfidf_array[:-1])
    bag_comment_and_rule_tfidf_array_pca = pca.transform(bag_comment_and_rule_tfidf_array)


    
    
    distance_matrix = cal_distance_matrix(bag_comment_and_rule_array[:-1])
    distance_matrix_set = cal_distance_matrix(bag_comment_and_rule_set_array[:-1])
    distance_matrix_tfidf = cal_distance_matrix(bag_comment_and_rule_tfidf_array[:-1])
    
    distance_array = np.nanmean(distance_matrix, axis=1)
    distance_array = fill_nan_with_mean(distance_array)
    
    distance_array_set = np.nanmean(distance_matrix_set, axis=1)
    distance_array_set = fill_nan_with_mean(distance_array_set)
    
    distance_array_tfidf = np.nanmean(distance_matrix_tfidf, axis=1)
    distance_array_tfidf = fill_nan_with_mean(distance_array_tfidf)
    
    
    
    pca_distance_matrix = cal_distance_matrix(bag_comment_and_rule_array_pca[:-1])
    pca_distance_matrix_set = cal_distance_matrix(bag_comment_and_rule_set_array_pca[:-1])
    pca_distance_matrix_tfidf = cal_distance_matrix(bag_comment_and_rule_tfidf_array_pca[:-1])
    
    pca_distance_array = np.nanmean(pca_distance_matrix, axis=1)
    pca_distance_array = fill_nan_with_mean(pca_distance_array)
    
    pca_distance_array_set = np.nanmean(pca_distance_matrix_set, axis=1)
    pca_distance_array_set = fill_nan_with_mean(pca_distance_array_set)
    
    pca_distance_array_tfidf = np.nanmean(pca_distance_matrix_tfidf, axis=1)
    pca_distance_array_tfidf = fill_nan_with_mean(pca_distance_array_tfidf)
    
    
    
    
    comments_df['count distance'] = distance_array
    comments_df['set distance'] = distance_array_set
    comments_df['tfidf distance'] = distance_array_tfidf
    comments_df['pca count distance'] = pca_distance_array
    comments_df['pca set distance'] = pca_distance_array_set
    comments_df['pca tfidf distance'] = pca_distance_array_tfidf
    
    count_similarity_array = []
    set_similarity_array = []
    tfidf_similarity_array = []
    pca_count_similarity_array = []
    pca_set_similarity_array = []
    pca_tfidf_similarity_array = []
    
    for comment_i in range(len(comments_df)):
#        comments_df.loc[comment_i,'count similarity'] = calculate_similarity_count(bag_comment_and_rule_array,comment_i,-1)
#        comments_df.loc[comment_i,'set similarity'] = calculate_similarity_set(bag_comment_and_rule_set_array,comment_i,-1)
#        comments_df.loc[comment_i,'tfidf similarity'] = calculate_similarity_tfidf(bag_comment_and_rule_tfidf_array,comment_i,-1)
        count_similarity_array.append(calculate_similarity_count(bag_comment_and_rule_array,comment_i,-1))
        set_similarity_array.append(calculate_similarity_set(bag_comment_and_rule_set_array,comment_i,-1))
        tfidf_similarity_array.append(calculate_similarity_tfidf(bag_comment_and_rule_tfidf_array,comment_i,-1))
        pca_count_similarity_array.append(calculate_similarity_count(bag_comment_and_rule_array_pca,comment_i,-1))
        pca_set_similarity_array.append(calculate_similarity_set(bag_comment_and_rule_set_array_pca,comment_i,-1))
        pca_tfidf_similarity_array.append(calculate_similarity_tfidf(bag_comment_and_rule_tfidf_array_pca,comment_i,-1))
        
        
        
        
    comments_df['count similarity'] = fill_nan_with_mean(np.array(count_similarity_array))
    comments_df['set similarity'] = fill_nan_with_mean(np.array(set_similarity_array))
    comments_df['tfidf similarity'] = fill_nan_with_mean(np.array(tfidf_similarity_array))
    comments_df['pca count similarity'] = fill_nan_with_mean(np.array(pca_count_similarity_array))
    comments_df['pca set similarity'] = fill_nan_with_mean(np.array(pca_set_similarity_array))
    comments_df['pca tfidf similarity'] = fill_nan_with_mean(np.array(pca_tfidf_similarity_array))
    
        
        
    
    
    comments_df.fillna(0)
    
    similarity_save_add = similarity_save_basic_add +"\\similarity_"+"One"+"_" + str(rule_type_i) +".pickle"
#    pickle.dump(comments_df, open(similarity_save_add,"wb"))
    similarity_csv_save_add = similarity_save_add.replace(".pickle",".csv")
#    comments_df.to_csv(similarity_csv_save_add)
    
    count_distance_matrix_save_add = similarity_save_basic_add +"\\count_distance_matrix"+"One"+"_" + str(rule_type_i) +".pickle"
    set_distance_matrix_save_add = similarity_save_basic_add +"\\set_distance_matrix"+"One"+"_" + str(rule_type_i) +".pickle"
    tfidf_distance_matrix_save_add = similarity_save_basic_add +"\\tfidf_distance_matrix"+"One"+"_" + str(rule_type_i) +".pickle"
    pca_count_distance_matrix_save_add = similarity_save_basic_add +"\\pca_count_distance_matrix"+"One"+"_" + str(rule_type_i) +".pickle"
    pca_set_distance_matrix_save_add = similarity_save_basic_add +"\\pca_set_distance_matrix"+"One"+"_" + str(rule_type_i) +".pickle"
    pca_tfidf_distance_matrix_save_add = similarity_save_basic_add +"\\pca_tfidf_distance_matrix"+"One"+"_" + str(rule_type_i) +".pickle"
    
#    pickle.dump(distance_matrix, open(count_distance_matrix_save_add,"wb"))
#    pickle.dump(distance_matrix_set, open(set_distance_matrix_save_add,"wb"))
#    pickle.dump(distance_matrix_tfidf, open(tfidf_distance_matrix_save_add,"wb"))
#    pickle.dump(pca_distance_matrix, open(pca_count_distance_matrix_save_add,"wb"))
#    pickle.dump(pca_distance_matrix_set, open(pca_set_distance_matrix_save_add,"wb"))
#    pickle.dump(pca_distance_matrix_tfidf, open(pca_tfidf_distance_matrix_save_add,"wb"))
#    
    
#    pd.DataFrame(similarity_matrix).to_csv(similarity_matrix_save_add)


#    similarity_matrix_save_add = similarity_save_basic_add +"\\similarity_matrix"+"One"+"_" + str(rule_type_i) +".csv"
#    pd.DataFrame(similarity_matrix).to_csv(similarity_matrix_save_add)

    



#covariance = np.cov(comments_df[["count similarity","set similarity","tfidf similarity","count distance","set distance","tfidf distance"]].values, rowvar=False)
#correlation = np.corrcoef(comments_df[["count similarity","set similarity","tfidf similarity","count distance","set distance","tfidf distance"]].values.T)



#with open(similarity_save_add,"rb") as f:
#    tem=pickle.load(f, encoding='latin1')



















