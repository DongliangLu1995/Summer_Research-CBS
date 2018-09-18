# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 09:41:54 2018

@author: DongliangLu
"""

#this function separate the paragraph of the final rule
#you can view table of content list, and get to whichever section you want
import pickle
import numpy as np
import pandas as pd
import re
import os

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string

stop = stopwords.words("english")


def is_frame(line):
    unique_words_pattern = re.compile("[A-Za-z]\s+")
    unique_number_pattern = re.compile("\d+\s+")
    fed_pattern = re.compile("Federal Register / Vol")
    var_pattern = re.compile("VerDate\s")
    
    words_span = re.match(unique_words_pattern,line)
    number_span = re.match(unique_number_pattern,line)
    federal_span = re.match(fed_pattern,line)
    var_span = re.match(var_pattern,line)
    if words_span:
        start = words_span.span()[0]
        end = words_span.span()[1]
        if line[start:end] == line:
            return 0
    if number_span:
        start = number_span.span()[0]
        end = number_span.span()[1]
        if line[start:end] == line:
            return 0
    if federal_span:
        return 0
    if var_span:
        return 0
    return 1
#st = rule_raw_text[360]
#st = rule_raw_text[50]
#st = rule_raw_text[82]
#st = rule_raw_text[78]
#st[re.match(unique_words_pattern,st).span()[0]: re.match(unique_words_pattern,st).span()[1]] == st
#st[re.match(unique_number_pattern,st).span()[0]: re.match(unique_number_pattern,st).span()[1]] == st

def is_new_section(paragraph, pattern1, pattern2):
    if re.match(pattern1, paragraph):
        return 1
    for p in pattern2:
        if p in paragraph[:6]:
            return 1
    return 0


    

def find_all_citation(paragraph,citation_pattern1,citation_pattern2 ):
    citation_number = []
    citation_1 = re.findall(citation_pattern1, paragraph)
    citation_2 = re.findall(citation_pattern2, paragraph)
    if citation_1:
        for c_i in citation_1:
            citation_number.append(c_i[c_i.find(".")+1:])
    if citation_2:
        for c_i in citation_2:
            citation_number.append(c_i[c_i.find(".")+1:])
    return citation_number

def citation_num_to_org(citation_list, citation_to_org):
    org_list = []
    for citation_i in citation_list:
        if citation_i in citation_to_org:
            org_list.extend(citation_to_org[citation_i])
    return org_list

def Title(line):
    return " ".join([i[0].upper() + i[1:] for i in line.split()])

def is_agency(paragraph, agency_pattern_list):
    for a in agency_pattern_list:
        if a in paragraph:
            return 1
    return 0

def is_commentor(paragraph, commenter_pattern_list):
    for c in commenter_pattern_list:
        if c in paragraph:
            return 1
    return 0

def is_start_sentence(line, sub_section1, sub_section2):
    if re.match(sub_section1,line):
        return 1
    for start in sub_section2:
        if start in line[:4]:
            return 1
    start_P=re.compile("[A-Z]")
    if re.match(start_P,line[0]):
        return 1
    return 0

#def is_end(line,stop,title_ind):
def is_end(line,stop):
    if "." in line[-7:]:
        tem_line = line[-7:]
        location = tem_line.find(".")
        tem_line = tem_line[location:]
        word_pattern = re.compile("[A-Za-z]")
        if not re.search(word_pattern, tem_line):
            return 1
#    else:
#        if len(line.split())<=3:
#            tem_line = " ".join([i for i in line.split() if i not in stop])
#            if tem_line ==tem_line.title():
#                return 1
#    if title_ind and not belong_to_title(line, sub_section1, sub_section2,stop):
#        return 1
    return 0

#def check_upper(line, stop):
#    line_first = line.split()[:15]
#    line_list = [i.lower() for i in line_first]
#    for word in line_list:
#        if word in stop:
#            if line.find(word.capitalize()):#may have several this word
#                if line.find(word.capitalize())==0:
#                    pass
#                else:
#                    if line[line.find(word.capitalize())-2]==".":
#                        pass
#                    else:
#                        line
                
    
    

#content = table_of_content_list
def extract_title(paragraph, content):
    new_p = []
    for title in content:
#        title_pattern = re.compile(title)
#        if re.match(title_pattern, paragraph):
#            end = re.match(title_pattern, paragraph).span()[1]
#            new_p.append(paragraph[:end])
#            paragraph = paragraph[end:].strip()
        if paragraph.find(title)==0:
            end = len(title)
            new_p.append(paragraph[:end])
            paragraph = paragraph[end:].strip()            
    new_p.append(paragraph)
    return new_p


def pure_content(paragraph, citation_pattern1, citation_pattern2):
    Month = ["Jan. ", "Feb. ", "Mar. ","Apr. ","May. ", "Aug. ", "Sep. ",
             "Oct. ", "Nov. ", "Dec. "]
    Month_r = ["Jan", "Feb", "Mar","Apr","May", "Aug", "Sep",
             "Oct", "Nov", "Dec"]
    paragraph = paragraph.replace("U.S.","US")
    for m in range(len(Month)):
        paragraph = paragraph.replace(Month[m], Month_r[m])
    not_citation = ["I.","II.","III.","IV.","V.", "i.", "ii.", "iii.",
                "iv.","v.","ll.","l."]
    citation_1 = re.findall(citation_pattern1, paragraph)
    citation_2 = re.findall(citation_pattern2, paragraph)
    citation_num = []
    if citation_1:
        for c_i in citation_1:
            n_c_ind = 0
            for n_c in not_citation:
                if c_i.find(n_c) == 0:
                    n_c_ind = 1
            if n_c_ind == 0:
                start = c_i.find(".")
                paragraph = paragraph.replace(c_i[start:], ".")
                citation_num.append(c_i[start+1:])
        
    if citation_2:
        for c_i in citation_2:
            n_c_ind = 0
            for n_c in not_citation:
                if c_i.find(n_c) ==0:
                    n_c_ind = 1
            if n_c_ind == 0:
                start = c_i.find(",")
                paragraph = paragraph.replace(c_i[start:], ",") 
                citation_num.append(c_i[start+1:])
    return paragraph, citation_num




#def belong_to_title(line, sub_section1, sub_section2,stop):
#    if re.match(sub_section1,line):
#        return 1
#    for start in sub_section2:
#        if start in line[:4]:
#            return 1
#    new_line = " ".join([i for i in line.split() if i not in stop])
#    if new_line == Title(new_line):
#        return 1
#    return 0



#def paragraph_to_sentence(paragraph):
#    citation_pattern1 = re.compile("\.\d+")
#    citation_pattern2 = re.compile("\,\d+")



rule_type_i = 10


#see whcih organization is cited in this citation
citation_to_org={}
comments_save_basic_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\download\SEC_comments"
location_save_pickle_add_i = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_citation_location_"+str(rule_type_i)+".pickle"
with open(location_save_pickle_add_i,"rb") as f:
    tem=pickle.load(f)  
org_citation_location = tem
for org in org_citation_location.keys():
    for citation_num in org_citation_location[org]:
        if citation_num in citation_to_org:
            citation_to_org[citation_num].append(org)
        else:
            citation_to_org[citation_num] = [org]


final_rule_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\final rule\SEC_rule\final" + "\\"+str(rule_type_i)+ ".txt"
with open(final_rule_add, "r") as f:
    rule_raw_text = f.readlines()
    
#get rid of the pdf format frames
#such as unique words, unique numbers, VerDate, Federal Register
paragraph_list = []
end_list_ind = 0
tem_list = []
for line in rule_raw_text:
    if is_frame(line):
        if line !="\n":
            tem_list.append(line)
        else:
            if tem_list != []:
                paragraph_list.append(tem_list)
                tem_list = []


#identify whether this paragraph is a citation paragraph or not

citation_paragraph_list = []
main_rule_list = []
citation_pattern = re.compile("\d+\s\See")

for line_list in paragraph_list:
    citation_ind = 0
    for line in line_list:
        if re.match(citation_pattern, line):
            citation_ind=1
    if citation_ind==1:
        citation_paragraph_list.extend(line_list)
    else:
        main_rule_list.extend(line_list)


citation_separate = []
tem_c=""
for line_c in citation_paragraph_list:
    if re.match(citation_pattern, line_c):
        if tem_c !="":
            citation_separate.append(tem_c.replace("\n"," "))
        tem_c = line_c
        
    else:
        tem_c += line_c
#have some bugs with citation that don't start with number + See


table_of_content = main_rule_list[131:588]
background = main_rule_list[588:665]
overview = main_rule_list[665:1793]
final_rule = main_rule_list[1793:39913]
appendix = main_rule_list[39913:]

#for i in range(len(main_rule_list)):
#    if main_rule_list[i].find("PROPRIETARY TRADING")!=-1:
#        print(i)

sub_section1 = re.compile("[A-Za-z0-9]0*\.")
#sub_section2 = ["I. ","II. ","III. ","IV. ","V. ", "i. ", "ii. ", "iii. ",
#                "iv. ","v. "]
sub_section2 = ["I.","II.","III.","IV.","V.", "i.", "ii.", "iii.",
                "iv.","v."]
#re.match(sub_section,"A. a")

table_of_content_list = []
tem_content = ""
for content in table_of_content:
    if is_new_section(content, sub_section1, sub_section2):
        table_of_content_list.append( " ".join([i for i in tem_content.split()]).replace("- ","-").replace("funds","Funds").replace("customers","Customers").replace("To","to"))
        tem_content = content
    else:
        if content.split()[0].lower in stop:
            content = content[0].lower() + content[1:]
        tem_content+=content


#table_of_content_list2 = []
#for content in table_of_content_list:
#    content2 = " ".join( [Title(i)*(i not in stop and "." not in i)+i*(i in stop or "." in i) for i in content.split()]  )
#    if content2!=content:
#        print(content)


#separate_rule_paragraph
end_of_sentence_ind = 1
paragraph_list = []
new_sentence = ""
title_ind = 1
for line in final_rule:
    if end_of_sentence_ind and is_start_sentence(line, sub_section1, sub_section2):
        if new_sentence !="":
            paragraph_list.append( " ".join([i for i in new_sentence.replace("\n","").split()]).replace("- ","-") )
        new_sentence = line
    else:
        new_sentence+=line
#    if is_end(line,stop, title_ind):
    if is_end(line,stop):
        end_of_sentence_ind = 1
    else:
        end_of_sentence_ind = 0
#    title_ind = belong_to_title(line, sub_section1, sub_section2,stop)
        
#extraxt_title
paragraph_list_new = []
for paragraph in paragraph_list:
    paragraph_list_new.extend(extract_title(paragraph, table_of_content_list))



by_section_list = []
tem_section = []
for paragraph in paragraph_list:
    if is_new_section(paragraph, sub_section1, sub_section2):
        if tem_section != []:
            by_section_list.append(tem_section)
        tem_section = [paragraph]
    else:
        tem_section.append(paragraph)
        
#count = 0
#for b in by_section_list:
#    count+=len(b)
        

citation_pattern1 = re.compile("[A-Za-z]+\.\d+")
citation_pattern2 = re.compile("[A-Za-z]+\,\d+")
commenter_pattern_list = ["Commenter", "Commenters", "commenter", "commenters","Others","Other commenters" ]
agency_pattern_list = ["Agency", "Agencies", "final rule", "response to"]

#commenter_list = []
#agency_list = []
#citation_cul = []
#agency_cul = []
#progress_proposal_ind = 1
#progress_commenter_ind = 1
#progress_agency_ind = 0

#for paragraph in paragraph_list:
#    tem_citation = find_all_citation(paragraph,citation_pattern1,citation_pattern2 )
#    citation_cul.extend(tem_citation)
#    if is_agency(paragraph, agency_pattern_list):
#        agency_cul.append(paragraph)
#        progress_commenter_ind = 0
#        progress_agency_ind = 1
#    else:
#        progress_commenter_ind = 1
#        progress_agency_ind = 0
#    if progress_commenter_ind == 1:
#        if agency_cul!=[]:
#            agency_list.append(agency_cul)
#            commenter_list.append(citation_num_to_org(citation_cul, citation_to_org))
#            citation_cul = []
#            agency_cul = []
#
#agency_list.append(agency_cul)
#commenter_list.append(citation_num_to_org(citation_cul, citation_to_org))
            
#commenter_list = []
#agency_list = []
#citation_cul = []
#agency_cul = []
#category = []
sentence_list = []
sentence_ind_list = []
citation_list = []
#0 for title, 1 for proposal rule, 2 for comments, 3 for results, 4 for both, 5 for undefined
#4 may either because the sentence contains both the comments and agencies, 
#or may because the agencies are saying directly the comments' advice is good or not
#or may because the commenters are asking the agencies to do something
for paragraph in paragraph_list_new:
    if paragraph in table_of_content_list:
        sentence_list.append(paragraph)
        sentence_ind_list.append(0)
        citation_list.append(0)
        
    else:
        paragraph_clean, citation_nums = pure_content(paragraph, citation_pattern1, citation_pattern2)
        tem = paragraph_clean.split(". ")
        tem_new = []
        for tem_i in range(len(tem)):
            if tem[tem_i]!="":
                if tem[tem_i][-1]!=".":
                    tem_new.append( tem[tem_i] + ".")
                else:
                    tem_new.append( tem[tem_i])
        sentence_list.extend(tem_new)
        for tem_i in range(len(tem_new)):
            citation_list.append(citation_nums)
            comment_ind = 0
            agency_ind = 0
            for com_p in commenter_pattern_list:
                if com_p in tem_new[tem_i]:
                    comment_ind = 1
            for age_p in agency_pattern_list:
                if age_p in tem_new[tem_i]:
                    agency_ind = 1
            if sentence_ind_list[-1] in [1, 0]:# should be proposed rule
                if comment_ind==0:
                    sentence_ind_list.append(1)
                else:
                    if agency_ind == 1:
                        sentence_ind_list.append(4)
                    else:
                        sentence_ind_list.append(2)
            else:
                if comment_ind == 1:
                    if agency_ind == 1:
                        sentence_ind_list.append(4)
                    else:
                        sentence_ind_list.append(2)
                elif agency_ind == 1:
                    sentence_ind_list.append(3)
                else:
                    sentence_ind_list.append(5)
                    
#if there is a 4 between a lot of 2, this 4 may because of commenters mentioned agency, but not the agency's result
F_T_pattern = ["Agencies should", "urged the Agencies"]
for s_i in range(len(sentence_ind_list)):
    if sentence_ind_list[s_i] == 4:
        for F_T_p in F_T_pattern:
            if F_T_p in sentence_list[s_i]:
                sentence_ind_list[s_i] = 2


pre_ind = 0
next_ind = 5
total_s = len(sentence_ind_list)
for s_i in range(total_s):
    if sentence_ind_list[s_i] == 4:
        for pre in range(1,s_i):
            if sentence_ind_list[s_i-pre] not in [4,5]:
                pre_ind = sentence_ind_list[s_i-pre]
                break
        for nex in range(1,total_s - s_i):
            if sentence_ind_list[s_i+nex] not in [4,5]:
                nex_ind = sentence_ind_list[s_i+nex]
                break            
        
        
        if pre_ind in [0,1]:
            sentence_ind_list[s_i] = 2
        elif pre_ind == 2 and nex_ind == 2:
            sentence_ind_list[s_i] = 2
        elif nex_ind == 0:
            sentence_ind_list[s_i] = 3
        else:
            pass
        
sentence_ind_list_old = [i for i in sentence_ind_list]

#mislabeled: finding the 4 that should be 2
#13, 14 should be 2 not 4, 13 gives the pattern "the Agencies should"
#14 gives the pattern "urged the Agencies"
#123 be 2, pattern "the agencies would", which is dangerous, but also a series of 2,4,5,2
#17 should be 3, but ok
#22 should be 3, but ok
#86 should be 2
#159, 160, be 2, gives 2,4,4,2
#173, 174 should be 3, 3,4,4,5,5,5,3
#207, 208 should be 2, 208 has contained "should", 2,4,4,3
#265 should be 3,
#solution: first deal with "should", "urged", and then deal with series




#identify the sentence which is labeld 5

    
tem_s_ind = []
pre_ind = 0
for s_i in range(len(sentence_ind_list)):
    
    if sentence_ind_list[s_i] == 5:
        tem_s_ind.append(s_i)
        if pre_ind in [0,1]:
            for tem_s_i in tem_s_ind:
                sentence_ind_list[tem_s_i] = 2
            tem_s_ind = []
        elif sentence_ind_list[s_i+1] in [3,4]:
            for tem_s_i in tem_s_ind:
                sentence_ind_list[tem_s_i] = 3
            tem_s_ind = []
        elif sentence_ind_list[s_i+1] == 5:
            pass
        elif sentence_ind_list[s_i+1] == 0:
            for tem_s_i in tem_s_ind:
                sentence_ind_list[tem_s_i] = 3
            tem_s_ind = []
        elif sentence_ind_list[s_i+1] == 2:
            if pre_ind == 2:
                for tem_s_i in tem_s_ind:
                    sentence_ind_list[tem_s_i] = 2
                tem_s_ind = []
            else:
                for tem_s_i in tem_s_ind:
                    sentence_ind_list[tem_s_i] = 3
                tem_s_ind = []                
        else:
            pass
    else:
        pre_ind = sentence_ind_list[s_i]
            
#for s_i in range(len(sentence_ind_list)):
#    if sentence_ind_list[s_i] == 5:
#        print(s_i)
            
        







comments_list = []
agency_list = []
comment_c = []
agency_c = []
change = 0
for ind_i in range(len(sentence_ind_list)):
    if sentence_ind_list[ind_i] == 2:
        comment_c.append(ind_i)
        if agency_c != []:
            agency_list.append(agency_c)
            agency_c = []
    elif sentence_ind_list[ind_i] in [3,4]:
        agency_c.append(ind_i)
        if comment_c != []:
            comments_list.append(comment_c)
            comment_c = []
    else:
        pass
agency_list.append(agency_c)

citation_list_corr = []
for part_i in range(len(agency_list)):
    citation_list_corr.append([])
    for part_ii in range(len(agency_list[part_i])):
        citation_list_corr[-1].extend(citation_list[agency_list[part_i][part_ii]])
    for part_ii in range(len(comments_list[part_i])):
        citation_list_corr[-1].extend(citation_list[comments_list[part_i][part_ii]])
    citation_list_corr[-1] = sorted(list(set(citation_list_corr[-1])))


# agency, failure, final rule, may be successful
failure = ["still", "Still", "However", "however", "not adopting", "retain",
           "retains", "continue", "not believe", "declined"]
#Finally, the Agencies have declined to adopt one commenter s recommendation that a position in a financial instrument be considered a trading account position only if it qualifies as a GAAP trading position.
success = ["adopted","changes","provides","modified","modifications","permit","refined",
           "crafted", "Agencies agree"]
#includes?
#success = ["final rule"]
#In response to these comments, the final rule provides that a purchase or sale by a banking entity that satisfies an existing delivery obligation of the banking entity or its customers, including to prevent or close out a failure to deliver, in connection with delivery, clearing, or settlement activity is not proprietary trading.
#To address these concerns, the final rule provides that proprietary trading does not include the purchase or sale of one or more financial instruments through a deferred compensation, stock-bonus, profit-sharing, or pension plan of the banking entity that is established and
#Accordingly, the final rule provides that proprietary trading does not include the purchase or sale of one or more financial instruments in the ordinary course of collecting a debt
#the final rule will permit banking entities to continue to provide beneficial market-making and underwriting services to customers, and therefore provide liquidity to customers and facilitate capital-raising.
#To respond to concerns raised by commenters while remaining consistent with Congressional intent, the final rule has been modified to provide that certain purchases and sales are not proprietary trading as described in more detail below. 
#In addition, the Agencies believe commenters concerns about the scope of the proposed definition of trading account are substantially addressed by the refined exemptions in the final rule for customer-oriented activities, such as market making-related activities, and the exclusions from proprietary trading.
#First, in response to comments, the final rule replaces the reference to an account that is presumed to be a trading account with the purchase or sale of a financial instrument.



#failure_or_not = []
#pending = []
#for result_i in range(len(agency_list)):
#    ind_l = agency_list[result_i]
#    s = ""
#    for sentence_i in ind_l:
#        s += sentence_list[sentence_i]
#        s += " "
#    f_ind = 0
#    for f in failure:
#        if s.find(f) != -1:
#            f_ind = 1
#    failure_or_not.append(f_ind)
#    if not f_ind:
#        pending.append(s)
        
def is_success(part, success):
    s_ind = 0
    key_word = []
    if "final rule" in part:
        for suc in success:
            if suc in part:
                s_ind = 1
                key_word.append(suc)
    return s_ind, key_word


success_or_not = []
pending = []
success_lobby = []
success_key = []
lobbying_result_sentence = []
for result_i in range(len(agency_list)):
    ind_l = agency_list[result_i]
    s = ""
    for sentence_i in ind_l:
        s += sentence_list[sentence_i]
        s += " "
#    s_ind = 0
#    for f in success:
#        if s.find(f) != -1:
#            s_ind = 1
    s_ind,key_word = is_success(s, success)
    success_or_not.append(s_ind)
    if not s_ind:
        pending.append(s)
    else:
        success_lobby.append(s)
        success_key.append(key_word)
    lobbying_result_sentence.append(s)
        
    
#get the organizations result
org_cited_list = []
for c_i in range(len(agency_list)):
    org_cited = citation_num_to_org(citation_list_corr[c_i], citation_to_org)
    org_cited_list.append(org_cited)
    s_or_n_ind = success_or_not[c_i]
org_success_dic = {}
for c_i in range(len(agency_list)):
    for org in set(org_cited_list[c_i]):
        if org in org_success_dic:
            org_success_dic[org][0] += 1
            org_success_dic[org][1] += success_or_not[c_i]
        else:
            org_success_dic[org] = [1,success_or_not[c_i] ]
result_list = []
for org_i in org_success_dic.keys():
    result_list.append({})
    result_list[-1]["organization"] = org_i
    result_list[-1]["lobby times"] = org_success_dic[org_i][0]
    result_list[-1]["success times"] = org_success_dic[org_i][1]
    result_list[-1]["success rate"] = org_success_dic[org_i][1] / org_success_dic[org_i][0]
    
result_df = pd.DataFrame(result_list)
save_basic_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\lobby_success"
save_add = save_basic_add+"\\"+str(rule_type_i)+"_success_result.csv" 

result_df.to_csv(save_add,columns = ["organization", "lobby times", "success times"] )
        
lobby_sentence_related_org = []
for l_i in range(len(agency_list)):
    lobby_sentence_related_org.append([lobbying_result_sentence[l_i],set(org_cited_list[l_i])])

lobby_sentence_related_org_save_add = r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned\similar_paragraph_2"
lobby_sentence_related_org_save_add_i = lobby_sentence_related_org_save_add + "\\lobby_org" + str(rule_type_i) + ".pickle"
pickle.dump(lobby_sentence_related_org, open(lobby_sentence_related_org_save_add_i,"wb") )



with open(lobby_sentence_related_org_save_add_i,"rb") as f:
    tem=pickle.load(f)



#citations 2012),242


































