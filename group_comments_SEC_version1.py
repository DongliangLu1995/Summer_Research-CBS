# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 13:55:50 2018

@author: DongliangLu
"""

#group comments SEC
import pandas as pd
import re
import pickle
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import nltk
import string
#start to exit unexpectedly maybe it's the fuzzywuzzy library or the leivn
#try using tfidf

#use orginzations in meetings
#set rule type number using comments
#using matchit in stata

#to deal with org
#step1 lower and stem; remember to create a dic to trace back what it originally is
#step2 remove stop word

#don't forger to replace the new function in meeting here


data_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"
SEC_comments_data=pd.read_csv(data_add+"\\SEC_comments.csv",index_col=0)
SEC_meetings_data=pd.read_csv(data_add+"\\SEC_meetings.csv",index_col=0)

org_pickle=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_meeting_total.pickle"
with open(org_pickle,"rb") as f:
    tem=pickle.load(f, encoding='latin1')

org_clean=set(tem.keys())

new_org=["Prudential","Renaissance"]

#punctuation=list(string.punctuation)
#punctuation[:10]
stop1=stopwords.words("english")
#len(stop)=179
#stop[0:10]
stop2=["capital","financial","association","association","investment","asset",
       "management","group","industry","security","securities","risk","associ",
       "stor","associatio","manag","firm","forum","union","office","offices","advisor",
       "corporatio","institut","partn","compani","industri","fin","school","counsel",
       "america","gener","japans",'canada','australia',"partner","fund","ventur","capit",
       "nation","univers","consult","offic","union","labor","bank","staff"]
stop=stop1+stop2
stop=set(stop)
def remove_stop_words(word,stopword):
    #need to make sure the word is lowered
    word_o=word
    word_n=" ".join([i for i in word.split() if i not in stopword])

    if word.strip()=="":
        return word_o
    else:
        return word_n


porter_stemmer = PorterStemmer()
#porter_stemmer.stem("Senators Merkley and Levin's offices")

#for i in org_clean:
#    print()
#    print(i.lower())
#    print(porter_stemmer.stem(i.lower()))
#it's ok, no need to worry about that

#org_dic={}
#org_clean2=[]
#for org in org_clean:
#    org_n=org.lower()
#    org_n=porter_stemmer.stem(org_n)
#    org_n=remove_stop_words(org_n,stop)
#    org_dic[org_n]=org

def stem_org(org):
    org=org.lower()
    org=" ".join([porter_stemmer.stem(i) for i in org.split()])
    org=remove_stop_words(org,stop)
    return org




with open("US_major_cities.txt","r") as f:
    tem=f.readlines()
    
city_state=set()
for i in tem:
    i.strip()
    d_pattern=re.compile("\d")
    if not re.search(d_pattern, i ):# is a city or state
        try:
            i_l=i.split(";")
            i0=i_l[0].lower().strip()
            i1=i_l[1].lower().strip()
            city_state=city_state|set([i0,i1])
        except:
            i_l=i.split(",")
            i0=i_l[0].lower().strip()
            i1=i_l[1].lower().strip()
            city_state=city_state|set([i0,i1])

with open("american_states.txt","r") as f:
    tem=f.readlines()

for i in tem:
#    print(i.split("\t")[2].lower())
    city_state=city_state|set([i.split("\t")[2].lower()])


def is_org(org):
    not_org=["Wu",
             "Advisory",
             "As You Sow",
             "Change to Wi",
             "Consulting",
             "Free the Slaves",
             "Friends of the Congo",
             "Jr.",
             "LCH.Clearnet and Rich Feuer Group",
             "Lt",
             "Occupy the SEC",
             "PC",
             "Public Citize",
             "lm",
             "y",
             "A"
             "a",
             "Meeting of the OTC Derivatives Supervisors Group (ODSG) with major participants in the OTC derivatives market",
             "Executive Vice President"
            ]
    if org in not_org or org.startswith("certain"):
        return "individual"
    else:
        return org
    #start with certain
    
def sepe_and(org):
    and_comp=["DBRS and Pickard & Djinis",
              "Exxon Mobil Corporation and Shell International Limite",
              "Exxon Mobil Corporation and the Center on Executive Compensatio",
              "Financial Planning Association and the National Association of Personal Financial Advisors",
              "Financial Services Institute and LPL Financial",
              "Fund Democracy and the CFA",
              "Global Witness and Publish What You Pay",
              "Global Witness and The One Campaig",
              "ICE Inc. and Creditex",
              "ICE Trust and the Intercontinental Exchange, Inc.",
              "ISDA and Kalorama Partners",
              "Institute of International Bankers and Cleary Gottlieb Steen & Hamilton LLP",
              "International Swaps and Derivatives Association and the Securities Industry and Financial Markets Associatio",
              "Investment Company Institute and FINRA",
              "National Venture Capital Association and Proskauer Rose LLP",
              "OTC Derivatives Regulators Forum members and certain central counterparties",
              "OTC Derivatives Regulators Forum members and certain central counterparties (CCPs)",
              "OTC Derivatives Regulators Forum members and certain trade repositories",
              "RBC Capital Markets and Sullivan &Cromwell LLP",
              "SVB Financial Group and Debevoise & Plimpton LLP",
              "State Farm and Arnold & Porter",
              "The Depository Trust & Clearing Corporatio",
              "Wells Fargo Advisors and First Clearing, LLC",
              "AFSCME and AFL-CIO",
              "American Benefits Council and CIEBA",
              "Assured Guaranty and the Association of Financial Guaranty Insurers",
              "Citadel LLC and Delta Strategy Group",
              "Citadel LLC and Winston & Strawn",
              "Institute of International Bankers and Cleary Gottlieb Steen & Hamilton",
              "Loan Syndications & Trading Association and WilmerHale",
              "SVB Financial Group and Debevoise & Plimpton",
              "Wells Fargo Advisors and First Clearing",
              "National Venture Capital Association and Proskauer Rose"
              ]
    if org in and_comp:
        orgs=org.split("and")
        return[i.strip() for i in orgs ]
    else:
        return org
   

def rewrite_orgname(org):
    strip_list=["Inc","Inc.","LP","L.P.","Co","Co.","LLP","& Co.",", Inc.","LLC","Corp.","&",","]

    if type(org)==str:
        t_pattern=re.compile("[Tt]he ")
        if re.match(t_pattern,org):
            org=org[4:]
        stop_i=1
        while stop_i:
            stop_i=len(strip_list)
            for sl in strip_list:
                if org.endswith(sl):
                    org=org.rstrip(sl).strip()
                    stop_i=len(strip_list)
                else:
                    stop_i-=1
        
        
        #org=org.capitalize()
#        not_an_org=("Firm","Public Citize","Public Citizen","Usaa")
        formal_name={"American Bakers' Association": "American Bankers Association",
                     "American bakers' association":"American Bankers Association",
                     "American for Financial Reform":"Americans for Financial Reform",
                     "Ameriprise Financial":"Ameriprise",
                     "Alternative Investment Management Association (AIMA)":"Alternative Investment Management Association",
                     "Alternative Investment Management Associatio":"Alternative Investment Management Association",
                     "American Petroleum Institute (API)":"American Petroleum Institute",
                     "AFL-CIO Office of Investment":"AFL-CIO",
                     "AFSCME Capital Strategies":"AFSCME",
                     "BB&T Capital Markets":"BB&T",
                     "BB&T Corporation":"BB&T",
                     "BMO Harris Bank N.A.":"BMO Financial",
                     "BMO Financial Corp.":"BMO Financial",
                     "BNY Mellon Corporation":"BNY Mellon",
                     "Bank Of New York Mellon":"BNY Mellon",
                     "BNY Mellon Clearing":"BNY Mellon",
                     "BNY/Mello":"BNY Mellon",
                     "BNY/Mell":"BNY Mellon",
                     "Bank of New York Mellon Corp.":"BNY Mellon",
                     "Bank Of New York Mellon":"BNY Mellon",
                     "Bank of Americ":"Bank of America Merrill Lynch",
                     "Bank of America":"Bank of America Merrill Lynch",
                     "Bank of America and Merrill Lynch":"Bank of America Merrill Lynch",
                     "Barclays Capital":"Barclays",
                     "Barclays Capital":"Barclays",
                     "Better Markets":"Better Markets",
                     "Best Buy":"Best Buy",
                     "BNY ConvergEx Group":"BNY Mellon",
                     "BP p.l.c.":"BP",
                     "BHP Billiton Ltd.":"BHP Billiton",
                     "BlackRock Inc.":"BlackRock",
                     "Blackrock":"BlackRock",
                     "Bloomberg L.P.":"Bloomberg",
                     "Bloomberg LP":"Bloomberg",
                     "Capstone LLC":"Capstone",
                     "Citi":"Citigroup",
                     "Citigroup Inc":"Citigroup",
                     "Citibank":"Citigroup",
                     "citibank":"Citigroup",
                     "Clearly Gottlieb":"Clearly",
                     "Chicago Mercantile Exchange Group":"CME",
                     "CME Group":"CME",
                     "Coalition for Derivatives End-Users":"Coalition for Derivatives End Users",
                     "Financial Planning Associatio":"Financial Planning Association",
                     "Comerica Incorporated":"Comerica",
                     "Comerica Securities":"Comerica",
                     "Consumer Federation of Americ":"Consumer Federation of America",
                     "Consumer Federation of America and other organizations":"Consumer Federation of America",
                     "Credit Suisse Group AG":"Credit Suisse",
                     "Credit Suisse Asset Management":"Credit Suisse",
                     "Credit Suisse Securities (USA)":"Credit Suisse",
                     "CFA Institute":"CFA",
                     "CFP Boar":"CFA",
                     "Davis Polk":"Davis Polk & Wardwell",
                     "Davis, Polk & Wardwell":"Davis Polk & Wardwell",
                     "Davis Polk & Wardwell LLP":"Davis Polk & Wardwell",
                     "Debevoise":"Debevoise & Plimpton",
                     "Debevoise &amp":"Debevoise & Plimpton",
                     "Depository Trust & Clearing Corporatio":"Depository Trust Clearing Corporatio",
                     "Deutsche Bank AG New York":"Deutsche Bank",
                     "Deutsche Bank Americas":"Deutsche Bank",
                     "Deutsche Bank Americas Corp.":"Deutsche Bank",
                     "Deutsche Bank and Sidley Austi":"Deutsche Bank",
                     "D. E. Shaw & Co., LLP":"D.E. Shaw",
                     "D. E. Shaw":"D.E. Shaw",
                     "Depository Trust and Clearing Corporatio":"Depository Trust Clearing Corporatio",
                     "Discovery":"Discovery Capital Management",
                     "Discover Financial Services":"Discovery Capital Management",
                     "EquiLe":"Equile",
                     "ExxonMobil":"Exxon Mobil",
                     "Exxon Mobil Corporation":"Exxon Mobil",
                     "Fidelity Investments":"Fidelity",
                     "Financial Services Roundtable and constituent members":"Financial Services Roundtable",
                     "Financial Services Institute, Inc.":"Financial Services Institute",
                     "GE Capital Corp.":"GE",
                     "GE Capital":"GE",
                     "General Electrc Co.":"General Electric",
                     "Sachs":"Goldman Sachs",
                     "State Farm VP Management":"State Farm",
                     "Sachs & Co. and Goldman Sachs Execution & Clearing":"Goldman Sachs",
                     "Goldm":"Goldman Sachs",
                     "Goldman Sachs Group":"Goldman Sachs",
                     "Gunderson Dettmer Stough Villeneuve Franklin & Hachigi":"Gunderson Dettmer",
                     "General Electrc":"General Electric",
                     "HSBC Global Banking and Markets":"HSBC",
                     "HSBC Securities (USA) Inc.":"HSBC",
                     "HSBC Securities, (USA Inc.":"HSBC",
                     "Hartford Financial Services Group Inc":"Hartford",
                     "Investent Company Institute":"Investment Company Institute",
                     "Institute of International Bankers (IIB)":"Institute of International Bankers",
                     "International Swaps and Derivatives Associatio, Inc.":"International Swaps and Derivatives Associatio",
                     "International Swaps and Derivatives Association (ISDA)":"International Swaps and Derivatives Associatio",
                     "Investment Adviser Association (IAA)":"Investment Adviser Associatio",
                     "Investment Advisers Associatio":"Investment Adviser Associatio",
                     "Investment Company Institute and its Members":"Investment Company Institute",
                     "ISLA (International Securities Lending Association)":"ISLA",
                     "ICE Link":"ICE",
                     'Industry and Financial Markets Association ("SIFMA")':"SIFMA",
                     "International Swaps":"International Swaps and Derivatives Associatio",
                     "J.P. Morg":"J.P. Morgan",
                     "J.P. Morgan Chase":"J.P. Morgan",
                     "JPMorg":"J.P. Morgan",
                     "JPMorgan Chase & Co.":"J.P. Morgan",
                     "JPMorgan Chase & Co. regarding OTC Derivative Legislation":"J.P. Morgan",
                     "JPMorgan Chase & Co. regarding OTC Derivative Legislatio":"J.P. Morgan",
                     "JP Morg":"J.P. Morgan",
                     "JP Morgan":"J.P. Morgan",
                     "JP Morgan Chase":"J.P. Morgan",
                     "JPMorgan":"J.P. Morgan",
                     "JPMorgan Chase":"J.P. Morgan",
                     "Jp Morgan Chase":"J.P. Morgan",
                     "Jefferies & Company":"Jefferies",
                     "LLP; and Kenney & McCafferty":"Kenney & McCafferty",
                     "Laborers?? International Union of North Americ":"International Union of North Americ",
                     "Levin and 			Markey":"Levin Institute",
                     "Loomis, Sayles":"Loomis Sayles",
                     "Loomis, Sayles  L.P.":"Loomis Sayles",
                     "MFA":"Managed Funds Associatio",
                     "Managed Funds Association (MFA)":"Managed Funds Associatio",
                     "Markit":"MarkitSERV",
                     "Merrill Lynch, Pierce, Fenner & Smith Inc.":"Bank of America Merrill Lynch",
                     "Metlife":"MetLife",
                     "Morgan Stanley Smith Barney":"Morgan Stanley",
                     "Motorola Solutions":"Motorol",
                     "Motorol, Inc.":"Motorol",
                     'National Association of Insurance Commissioners ("NAIC")':"National Association of Insurance Commissioners",
                     "National Association of Insurance Commissioners (NAIC)":"National Association of Insurance Commissioners",
                     'National Association of Insurance and Financial Advisors ("NAIFA")':"National Association of Insurance and Financial Advisors",
                     "Nationwide Insurance and Financial Services Inc":"Nationwide Financial Services",              
                     "Nationwide":"Nationwide Financial Services",
                     "Nationwide Investment":"Nationwide Financial Services",
                     "National Venture Capital Association":"National Venture Capital Associatio",
                     "National Venture Capital Association.":"National Venture Capital Associatio",
                     "New York Stock Exchange":"NYSE",
                     "Nomur":"Nomura",
                     "Nomura Holding America Inc. and Nomura Securities International":"Nomura",
                     "Nomura Holding America":"Nomura",
                     "Nomura Securities International":"Nomura",
                     "Northern Trust Corporation":"Northern Trust",
                     "Northern Trust Company":"Northern Trust",
                     "North American Securities Administration Associatio":"North American Securities Administrators Associatio",
                     "North American Securities Administrators Associatio, Inc.":"North American Securities Administrators Associatio",
                     'North American Securities Administrators Association ("NASAA")"':"North American Securities Administrators Associatio",
                     "PNC Financial Services Group, Inc.":"PNC",
                     "PNC Financial Services Group Inc":"PNC",
                     "Principal Financial Group":"Principal",
                     "Private Equity Growth Company Council":"Private Equity Growth Capital Council",
                     "Promontory Financial Group":"Promontory Financial",
                     "Prudential Financial":"Prudential",
                     "Publish What You Pay":"Publish What You Pay Coalitio",
                     "Putnam Investments Inc":"Putnam",
                     "Putnam  Investments":"Putnam",
                     "RBC Capital Markets":"RBC",
                     "RBC Wealth Management - U.S.":"RBC",
                     "RBC Capital Markets and Sullivan &Cromwell":"RBC",
                     "RBS Securities Inc":"RBS",
                     "RBS Americas":"RBS",
                     "RBS Global Banking and Markets":"RBS",
                     "Royal Bank of Canada":"RBC",
                     'Risk Management Association ("RMA")':'Risk Management Association',
                     "Risk Management Association (RMA)":'Risk Management Association',
                     "RiskMetrics Group, Inc.":"RiskMetrics Group",
                     "Royal Bank of C":"RBC",
                     "Royal Dutch Shell plc":"Royal Dutch Shell",
                     "SIFMA and David Polk":"SIFMA",
                     "Capital Steering Committee of the Securities Industry and Financial Markets Association (SIFMA)":"SIFMA",
                     "Board of SIFMA":"SIFMA",
                     "Securities Industry and Financial Markets Associatio":"SIFMA",
                     'Securities Industry and Financial Markets Association ("SIFMA") and SIFMA Member Firms':"SIMFA",
                     "Securities Industry and Financial Markets Association (SIFMA)":"SIFMA",
                     "Securities Industry and Financial Markets Association (SIFMA) and Davis Polk & Wardwell LLP":"SIFMA",
                     "SIMFA":"SIFMA",
                     "State Street":"State Street Bank & Trust Company",
                     "State Street Corporation":"State Street Bank & Trust Company",
                     "State Street Global Advisors":"State Street Bank & Trust Company",
                     "Standard and Poor's Ratings Services":"Standard & Poor's Rating Services",
                     "State Farm VP Management Corp.":"State Farm",
                     "Stephens Inc.":"Stephens",
                     "Sulllivan & Cromwell LLP":"Sullivan & Cromwell",
                     "Sullivan and Cromwell":"Sullivan & Cromwell",
                     "Sullivan & Cromwell Llp":"Sullivan & Cromwell",
                     "Sun Guar":"SunGar",
                     "Swaps and Derivatives Market Association (SDMA)":"Swaps & Derivatives Market Association",
                     "Swaps & Derivatives Market Associatio":"Swaps & Derivatives Market Association",
                     "Representatives the Capital Steering Committee of the Securities Industry and Financial Markets Association (SIFMA)":"SIFMA",
                     'TWCMIG"':"TWCMIG",
                     "TD Ameritrade, Inc.":"TD Ameritrade",
                     "Tradeweb":"TradeWeb",
                     "The Clearing House Association":"Clearing House",
                     "The Clearing House Association. Llc":"Clearing House",
                     "The Clearing House Association Llc":"Clearing House",
                     "Tradeweb, LLC":"TradeWeb",
                     "UBS Bank USA":"UBS",
                     "Wells Fargo Advisors":"Wells Fargo",
                     "Wells Capital Management":"Wells Fargo",
                     "Wells Fargo Securities":"Wells Fargo",
                     "Western Asset Management Co.":"Western Asset Management",
                     "members of SIMFA":"SIFMA",
                     "the Financial Services Roundtable":"Financial Services Roundtable",
                     "Wholesale Markets Brokers?? Associatio":"Wholesale Market Brokers' Associatio"
                     
                     }
        
        if org in formal_name:
#            print("!!!")
            return is_org(formal_name[org])
        else:
            return is_org(org)
    else:
        return "default"

def strip_comma(inf):
    return inf.strip().strip(";").strip()

def capitalize_first(word):
    if len(word)>1:
        return word[0].upper()+word[1:]
    else:
        return word
    
      
    
def cal_abbreviation(abb,word):
    word=remove_stop_words(word,stop1)
    if len(word.split())>=len(abb):
        word_abb="".join([i[0].upper() for i in word.split()])
        return fuzz.ratio(word_abb,abb)#has some problem
    else:
        return 0
#cal_abbreviation("SIFMA","School International Financial Mathe Affi") 100
#cal_abbreviation("SIFMA","School of the International Financial Mathe Affi") 80

def is_abb(word):
    if word==word.upper() and len(word.split())==1:#word1 is an abbreviation
        return 1
    else:
        return 0

def ratio_abbreviation(word1,word2):
    if is_abb(word1) and not is_abb(word2):#word1 is an abbreviation
        return cal_abbreviation(word1,word2)
    if is_abb(word2) and not is_abb(word1):
        return cal_abbreviation(word2,word1)
    if is_abb(word1) and is_abb(word2):
        return 100 if word1==word2 else 0
    return 0
    
def is_city(word,city_state):
    if word.lower() in city_state:
        return 1
    else:
        return 0
    
job_title=["MBA","President","CEO","Officer","Executive","Chief","VP","CFP","CLU","CPA",
           "CFP(R)","NAIFA","FPA","CSA","CHFC"]
job_title=[i.lower() for i in job_title]
def is_job(word,job_title):
    for i in job_title:
        if i in word.lower():
            return 1
    return 0
    
def contain_barcket(word):
    if "(" in word and ")" in word:
        word=word[word.find("(")+1:word.find(")")]
        return word.upper()
    else:
        return word
    
def match_org(org, Org_l,threshold):
    org=contain_barcket(org)
    score=0
    score2=0
    part_score=0
    org_mat="individual"
    org_stem=stem_org(org)
    try2=0
    if len(org_stem.split())==1:
        try2=1
        org_stem=org_stem.upper()
    
    for Org in Org_l:
        
        if is_abb(Org):
            if ratio_abbreviation(org,Org)>=85 or try2*ratio_abbreviation(org_stem,Org):
                return [1,Org]
        else:
            part_score_t=fuzz.partial_ratio(stem_org(org),stem_org(Org))
            score_t=fuzz.ratio(stem_org(org),stem_org(Org))
            score2_t=fuzz.ratio(org,Org)
            if part_score_t >= 80 and score_t>=threshold:
                if score2_t>=score2:
                    score=score_t
                    part_score=part_score_t
                    score2=score2_t
                    org_mat=Org
    if part_score >= 80 and score>=threshold and score2>=40:
        return [1, org_mat]
    else:
        return [0,"individual"]
    
def add_org(org,dic):
    if org in dic:
        dic[org]+=1
    else:
        dic[org]=1

#c="Center for Capital Markets Competitiveness"
#[1, 'GE Capital']
#fuzz.partial_ratio(c,"GE Capital") 80



#fuzz.ratio("this is a test", "this is a test!") 97 order does not matter
#fuzz.partial_ratio("this is a test", "this is a test!") 100
#fuzz.ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear") 91
#fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear") 100
#fuzz.token_sort_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear") 84
#fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear") 100

#choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
#process.extract("new york jets", choices, limit=2)
#[('New York Jets', 100), ('New York Giants', 78)]
#process.extractOne("cowboys", choices)
#("Dallas Cowboys", 90)

#fuzz.partial_ratio("Saad Inter Financial Mathe Asso", "SIFMA") 20
    


rule_type_dic={}
rule_type_list=SEC_comments_data["rule type"].unique()
for i in range(len(rule_type_list)):
    rule=rule_type_list[i]
    rule_type_dic[rule]=i

#save_pickle_add0=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_rule_dic.pickle"
#pickle.dump(rule_type_dic, open(save_pickle_add0,"wb"))
#with open(save_pickle_add0,"rb") as f:
#    tem=pickle.load(f, encoding='latin1')

threshold=50
count=0
amb_match_dic=[]
SEC_comment_org=[]
#for i in range(len(SEC_comments_data)):
#no_match=[]

#rule_type_list=SEC_comments_data["rule type"].unique()
##for i in range(500,1000):
#for rule in rule_type_list:
#    small_dataframe=SEC_comments_data[SEC_comments_data["rule type"]==rule]
#    small_group_result={}
#    for index, row in small_dataframe.iterrows():
#        
##    if i%100==0:
##        print(i)
#        match_i=0
##        rule_type=SEC_comments_data.loc[i,"rule type"]
#        rule_type=row["rule type"]
#        rule_type_num=rule_type_dic[rule_type]
#        org_inf=row["people"]
#        org_inf_l=org_inf.split(",")
#    #    find_or_not=0
#        for org_candidate in org_inf_l:
#    #        if not find_or_not:
#            org_candidate=strip_comma(org_candidate)
#            org_candidate=rewrite_orgname(org_candidate)
#    #        print(org_candidate)
#            if (not is_city(org_candidate,city_state))  and not is_job(org_candidate,job_title):
#                if org_candidate in org_clean:
#    #                count+=1
#                    match_i=1
#                    SEC_comment_org.append({})
#                    SEC_comment_org[-1]["orginzation"]=org_candidate
#                    SEC_comment_org[-1]["rule type"]=rule_type
#                    SEC_comment_org[-1]["rule type number"]=rule_type_num
#                   
#                else:
#    #                org_candidate=org_candidate.lower() 
#                    success_i,org_m = match_org(org_candidate, org_clean,threshold)
#    #                count+=success_i
#                    if success_i:
#    #                    amb_match_dic.append({org_candidate:org_m})
#                        match_i=1
#                        SEC_comment_org.append({})
#                        SEC_comment_org[-1]["orginzation"]=org_m
#                        SEC_comment_org[-1]["rule type"]=rule_type
#                        SEC_comment_org[-1]["rule type number"]=rule_type_num
#                        
#        if not match_i:
#    #        no_match.append(SEC_comments_data.loc[i,"people"])
#            SEC_comment_org.append({})
#            SEC_comment_org[-1]["orginzation"]="Individual"
#            SEC_comment_org[-1]["rule type"]=rule_type
#            SEC_comment_org[-1]["rule type number"]=rule_type_num 
#    save_pickle_add_i=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_comments_rule_"+str(rule_type_num)+".pickle"
#    pickle.dump(SEC_comment_org, open(save_pickle_add_i,"wb"))   


rule_type_list=SEC_comments_data["rule type"].unique()
#for i in range(500,1000):
for i in range(35,len(rule_type_list)):
    rule=rule_type_list[i]
    small_dataframe=SEC_comments_data[SEC_comments_data["rule type"]==rule]
    small_group_result={}
    for index, row in small_dataframe.iterrows():
        
#    if i%100==0:
#        print(i)
        match_i=0
#        rule_type=SEC_comments_data.loc[i,"rule type"]
        rule_type=row["rule type"]
        rule_type_num=rule_type_dic[rule_type]
        org_inf=row["people"]
        org_inf_l=org_inf.split(",")
    #    find_or_not=0
        for org_candidate in org_inf_l:
    #        if not find_or_not:
            org_candidate=strip_comma(org_candidate)
            org_candidate=rewrite_orgname(org_candidate)
    #        print(org_candidate)
            if (not is_city(org_candidate,city_state))  and not is_job(org_candidate,job_title):
                if org_candidate in org_clean:
    #                count+=1
                    match_i=1
                    add_org(org_candidate,small_group_result)
#                    SEC_comment_org.append({})
#                    SEC_comment_org[-1]["orginzation"]=org_candidate
#                    SEC_comment_org[-1]["rule type"]=rule_type
#                    SEC_comment_org[-1]["rule type number"]=rule_type_num
                   
                else:
    #                org_candidate=org_candidate.lower() 
                    success_i,org_m = match_org(org_candidate, org_clean,threshold)
    #                count+=success_i
                    if success_i:
    #                    amb_match_dic.append({org_candidate:org_m})
                        match_i=1
                        add_org(org_m,small_group_result)
#                        SEC_comment_org.append({})
#                        SEC_comment_org[-1]["orginzation"]=org_m
#                        SEC_comment_org[-1]["rule type"]=rule_type
#                        SEC_comment_org[-1]["rule type number"]=rule_type_num
                        
        if not match_i:
            add_org("Individual",small_group_result)
    #        no_match.append(SEC_comments_data.loc[i,"people"])
#            SEC_comment_org.append({})
#            SEC_comment_org[-1]["orginzation"]="Individual"
#            SEC_comment_org[-1]["rule type"]=rule_type
#            SEC_comment_org[-1]["rule type number"]=rule_type_num 
    small_group_result_list=[]
    for key in small_group_result.keys():
        small_group_result_list.append({})
        small_group_result_list[-1]["organization"]=key
        small_group_result_list[-1]["meeting times"]=small_group_result[key]
        small_group_result_list[-1]["rule type"]=rule_type
        small_group_result_list[-1]["rule type number"]=rule_type_num
        
    save_pickle_add_i=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_comments_rule_"+str(rule_type_num)+".pickle"
    pickle.dump(small_group_result_list, open(save_pickle_add_i,"wb"))   






        
#SEC_comments_all=pd.DataFrame(SEC_comment_org)
#                    
#save_pickle_add_c=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_comments_small_rule.pickle"
#pickle.dump(SEC_comments_all, open(save_pickle_add_c,"wb"))
#with open(save_pickle_add_i,"rb") as f:
#    tem=pickle.load(f, encoding='latin1')
        
        
        
        
        
        






























