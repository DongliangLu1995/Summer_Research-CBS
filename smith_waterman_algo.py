# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 15:49:28 2018

@author: DongliangLu
"""

#smith-waterman algorithm

import numpy as np

substi_score_m=3#ai=bj
substi_score_n=-3#ai!=bj

#here we suppose linear gap penalty
w=2


s1='TGTTACGG'
s2='GGTTGACTA'

def subs_score(a,b,score_match,score_notmatch):
    return score_match if a==b else score_notmatch


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



















































