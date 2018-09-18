# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:49:28 2018

@author: DongliangLu
"""

#smith-waterman algorithm

import numpy as np
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()
porter_stemmer.stem("america")
porter_stemmer.stem("americ")
porter_stemmer.stem("american")

substi_score_m=3#ai=bj
substi_score_n=-3#ai!=bj

#here we suppose linear gap penalty
w=2


s1='TGTTACGG'
s2='GGTTGACTA'


#edit distance
#https://leetcode.com/problems/edit-distance/description/

s1 = "python"
s2 = "pyrhon"

high = 3
low = -3


def subs_score(a,b,score_match,score_notmatch):
    return score_match if a==b else score_notmatch


from heapq import heappush, heappop
def minDistance(word1, word2):
    """
    :type word1: str
    :type word2: str
    :rtype: int
    """
    heap = [(0, word1, word2)]
    visited = set()
    while heap:
        d, w1, w2 = heappop(heap)
        if (w1, w2) in visited:
            continue
        visited.add((w1, w2))    
        if w1 == w2:
            return d
        if w1 and w2 and w1[0] == w2[0]:
            heappush(heap, (d, w1[1:], w2[1:]))
        else:
            if w1: heappush(heap, (d+1, w1[1:], w2)) #delete
            if w1 and w2: heappush(heap, (d+1, w1[1:], w2[1:])) #replace
            if w2: heappush(heap, (d+1, w1, w2[1:])) #add

#Input: word1 = "intention", word2 = "execution"
#Output: 5
#Explanation: 
#intention -> inention (remove 't')
#inention -> enention (replace 'i' with 'e')
#enention -> exention (replace 'n' with 'x')
#exention -> exection (replace 'n' with 'c')
#exection -> execution (insert 'u')


#Input: word1 = "horse", word2 = "ros"
#Output: 3
#Explanation: 
#horse -> rorse (replace 'h' with 'r')
#rorse -> rose (remove 'r')
#rose -> ros (remove 'e')


def find_match_score(s1, s2, high=3, low=-3):
    l1 = len(s1)
    l2 = len(s2)
    
    if l1>l2:
        s1, s2 = s2, s1
        l1, l2 = l2, l1
    #keep s1 be the shorter one
    if s1[0] != s2[0]:
        percent = 0
    else:
        percent = 1 - minDistance(s1, s2)/l2
        
    print(high)
    print(low)
    score = low + percent*(high - low)
    return score

find_match_score("python","pyrhon",high,low)
find_match_score("securities","security",high,low)
find_match_score("regulation","calculation",high,low)
find_match_score("a","b",high,low)
find_match_score('america','american',high,low)

#%%


H=np.zeros((len(s1)+1, len(s2)+1) )
n,m=H.shape
for i in range(1,n):
    for j in range(1,m):
        score1 = H[i-1,j-1] + subs_score(s1[i-1],s2[j-1],substi_score_m,substi_score_n)
        score2 = H[i-1,j] - w
        score3 = H[i,j-1] - w
        score4 = 0
        H[i,j] = max(score1,score2,score3,score4)

#trace back
trace_back_index=[]
max_index=np.where(H==np.max(H))
r_index=max_index[0][0]
c_index=max_index[1][0]
trace_back_index.append( (r_index, c_index) )
score_now=np.max(H)
while score_now >0:
    score1=H[r_index-1,c_index-1]
    score2=H[r_index-1,c_index]
    score3=H[r_index,c_index-1]
    score_now=max(score1,score2,score3)
    if max(score1,score2,score3)==score1:#what about the same score
        r_index-=1
        c_index-=1
    elif max(score1,score2,score3)==score2:
        r_index-=1
    else:
        c_index-=1
    trace_back_index.append( (r_index,c_index) )
        
#print
share=""
s1_fraction_index=[]
s2_fraction_index=[]
for i in range(len(trace_back_index)-1):
    if not s1_fraction_index or s1_fraction_index[-1] !=trace_back_index[i][0]:
        s1_fraction_index.append( trace_back_index[i][0] )
    if not s2_fraction_index or s2_fraction_index[-1] !=trace_back_index[i][1]:
        s2_fraction_index.append( trace_back_index[i][1] )
        
        
s1_takeout="".join(s1[i-1] for i in s1_fraction_index)[::-1]
s2_takeout="".join(s2[i-1] for i in s2_fraction_index)[::-1]
print(s1_takeout)
print(s2_takeout)






















































