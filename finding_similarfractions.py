# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 13:12:19 2018

@author: DongliangLu
"""

#finding similar fractions using smith waterman algo
import pandas as pd
import re
import numpy as np
import pickle

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

import string





def pdf_parse1(path):
    S=""
    fp = open(path, 'rb') 
    praser = PDFParser(fp)
    doc = PDFDocument()
    praser.set_document(doc)
    doc.set_parser(praser)
    doc.initialize()
    fp.close()
    if not doc.is_extractable:
        return None
    else:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        page_num=0
        for page in doc.get_pages(): 
            page_num+=1
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    results = x.get_text()
                    #print(len(results))
                    try:#if it is some format notation, ignore it
                        S+=results
                        S+="\n"
                    except:
                        pass
    return S,page_num






final_rule_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\final rule\SEC_rule\final"+"\\2.pdf"
comment1=r"C:\Users\DongliangLu\Desktop"+"\\sifma_rule2.pdf"


S1,n1=pdf_parse1(final_rule_add)
S2,n2=pdf_parse1(comment1)

#clean strings
porter_stemmer = PorterStemmer()

S1=[porter_stemmer.stem(i.lower()) for i in S1.split()]
S2=[porter_stemmer.stem(i.lower()) for i in S2.split()]

s1='Consistent with these operational\
concerns and the global nature of the\
security-based swap market, the\
available data appear to confirm that\
participants in this market are in fact\
active in market centers around the\
globe. Although, as noted above, the\
available data do not permit us to\
identify the location of personnel in a\
transaction, TIW transaction records\
indicate that firms that are likely to be\
security-based swap dealers operate out\
of branch locations in key market\
centers around the world, including\
New York, London, Tokyo, Hong Kong,\
Chicago, Sydney, Toronto, Frankfurt,\
Singapore and the Cayman Islands.60\
Given these market characteristics\
and practices, participants in the\
security-based swap market may bear\
the financial risk of a security-based\
swap transaction in a location different\
from the location where the transaction\
is arranged, negotiated, or executed, or\
where economic decisions are made by\
managers on behalf of beneficial\
owners. And market activity may occur\
in a jurisdiction other than where the\
market participant or its counterparty\
books the transaction. Similarly, a\
participant in the security-based swap\
market may be exposed to counterparty\
risk from a counterparty located in a\
jurisdiction that is different from the\
market center or centers in which it\
participates.'

s2='the jurisdiction where\
it manages that risk.62 Some financial\
groups may book transactions\
originating in a particular region to an\
affiliate established in a jurisdiction\
located in that region.Consistent with these operational\
concerns and the global nature of the\
security-based swap market, the\
available data appear to confirm that\
participants in this market sas are in fact\
active in market centers around the\
globe. Although, as noted as above, the\
available data do not permit us to\
identify the location of personnel in a\
transaction, TIW transaction records\
indicate that firms that csa are likely to be\
security-based swap dealers asa operate out\
of branch locations in key market\
centers around the world, including\
arising out of its dealing activity,\
it is likely to operate offices that\
perform sales or trading functions in\
one or more market centers'



substi_score_m=3#ai=bj
substi_score_n=-3#ai!=bj

#here we suppose linear gap penalty
w=2


#s1='TGTTACGG'
#s2='GGTTGACTA'

#s1=S1
#s2=S2

s1=s1.split()
s2=s2.split()

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
        
        
s1_takeout=" ".join([s1[i-1] for i in s1_fraction_index][::-1])
s2_takeout=" ".join([s2[i-1] for i in s2_fraction_index][::-1])
print(s1_takeout)
print(s2_takeout)











































