# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 16:34:17 2018

@author: DongliangLu
"""

#extra the information from pdf, doc or txt

#import os
import pandas as pd
import re
#import shutil
import numpy as np
import pickle

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
#read the pdf by columns, for example, content, citation,content,citation
#citations start from \n\n\d , seperate as \n, end in \n\n\^\d

#from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

from fuzzywuzzy import fuzz

import string

#steps to find the orginzations in the citation
#1. find the vocabulary in meetings' orginzation; stemlize them, add stop2; if there's a world that's unique, make a dic
#2. go through the final rule, stem the word, if there's a word belongs to the vocabulary, keep it(don't forget check the bracket)
#3. every time you find a word that's in the vocabulary and next is not, add 1
#4. split by 1, and check whether the world belongs to the unique dic,  ; if so, use the trick in comments 
#   which determining partial is org
#5. notice that orgs in final rule usually contains bracket, but here the content in the bracket, 
#   unlike org in SEC, here usually content contains no org inf, so we just ignore them.

#need to replace sth., for example, management into mgmt, associa... into ass


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
             "Executive Vice President",
             "President and CEO",
             "Americas",
             "State of Alask",
             "U.S. Insurer"
            ]
    if org in not_org or org.startswith("certain"):
        return "Individual"
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
              "National Venture Capital Association and Proskauer Rose",
              "Trade repositories (TRs) and ISDA",
              "Service Employees International Union; American Federation of State"
              ]
    if org in and_comp:
        if ";" not in org:
            orgs=org.split("and")
            return[i.strip() for i in orgs ]
        else:
            orgs=org.split(";")
            return[i.strip() for i in orgs ]            
    else:
        return org

def strip_pron(org):
#    pron=[",","'","."]
    if "&" in org:
        org = " ".join([i.strip() for i in org.split("&")])
    if "/" in org:
        org = " and ".join([i.strip() for i in org.split("/")])
    for p in punctuation:
        if p in org:
            org=org.replace(p,"")
    return org

def rewrite_orgname(org):
    strip_list=["Inc","Inc.","LP","L.P.","Co","Co.","LLP","& Co.",", Inc.","LLC","Corp.","&",","]

    if type(org)==str:
        t_pattern=re.compile("[Tt]he ")
        #don't use replace directly, or it will be some problem
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
                     "Caleb Gibson of Americans for Financial Reform":"Americans for Financial Reform",
                     "Ameriprise Financial":"Ameriprise",
                     "Alternative Investment Management Association (AIMA)":"Alternative Investment Management Association",
                     "Alternative Investment Management Associatio":"Alternative Investment Management Association",
                     "American Petroleum Institute (API)":"American Petroleum Institute",
                     "AFL-CIO Office of Investment":"AFL-CIO",
                     "AFSCME Capital Strategies":"AFSCME",
                     "BB&T Capital Markets":"BBT",
                     "BB&T Corporation":"BBT",
                     "BB T":"BBT",
                     "BMO Harris Bank N.A.":"BMO",
                     "BMO Financial Corp.":"BMO",
                     "BMO Financial":"BMO",
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
                     "Bond Dealers of Americ":"Bond Dealers of America",
                     "Board of Directors of the Bond Dealers of Americ":"Board of Directors of the Bond Dealers of America",
                     "Capstone LLC":"Capstone",
                     "Calvert Asset Management":"Calvert",
                     "Calvert Investments":"Calvert",
                     "Canadian Banks and the Canadian Bankers?? Associatio":"Canadian Banks and the Canadian Bankers Associatio",
                     'Center for Capital Markets Competitiveness event on "Over the Counter (OTC) Derivatives Reform: Preparing for a Changing Marketplace"':'Center for Capital Markets Competitiveness',
                     "Certified Financial Planner Board of Standards":"CFP",
                     "CFTC and certain pension plans":"CFTC",
                     "CRE Finance Council":"CRE",
                     "Center for Study of Financial Market Evolution (CSFME)":"CSFME",
                     "Conference call CRE Finance Council":"CRE",
                     "Citi":"Citigroup",
                     "Citigroup Inc":"Citigroup",
                     "Citibank":"Citigroup",
                     "citibank":"Citigroup",
                     "Clearly":"Clearly  Gottlieb",
                     "Chicago Mercantile Exchange Group":"CME",
                     "Cleary Gottlieb Steen Hamilto":"Cleary Gottlieb",
                     "Cleary Gottlieb & Steen Hamilto":"Cleary Gottlieb",
                     "Committee for the Fiduciary Standar":"Fiduciary Standar",
                     "Committee of Annuity Insurers regarding Business Conduct Standards":"Annuity Insurers",
                     "Commodity Futures Trading Commissio":"CFTC",
                     'Committee on Investment of Employee Benefit Assets\r\r\n(CIEBA)':"CIEBA",
                     'Conference of State Bank Supervisors ("CSBS")':"CSBS",
                     "Clients and the law firm of Gibso":"Gibso",
                     "CME Group":"CME",
                     "Coalition for Derivatives End-Users":"Coalition for Derivatives End Users",
                     "Fixed Income Forum and Credit Roundtable":"Credit Roundtable and Fixed Income Forum",
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
                     "Davis Polk":"Davis Polk Wardwell",
                     "Davis, Polk & Wardwell":"Davis Polk Wardwell",
                     "Davis Polk & Wardwell LLP":"Davis Polk Wardwell",
                     "Debevoise":"Debevoise Plimpton",
                     "Debevoise &amp":"Debevoise & Plimpton",
                     "Depository Trust & Clearing Corporatio":"Depository Trust Clearing Corporatio",
                     "Deutsche Bank AG New York":"Deutsche Bank",
                     "Deutsche Bank Americas":"Deutsche Bank",
                     "Deutsche Bank Americas Corp.":"Deutsche Bank",
                     "Deutsche Bank and Sidley Austi":"Deutsche Bank",
                     "D. E. Shaw & Co., LLP":"DE Shaw",
                     "D. E. Shaw":"DE Shaw",
                     "D.E. Shaw":"DE Shaw",
                     "Depository Trust and Clearing Corporatio":"Depository Trust Clearing Corporatio",
                     "Discovery":"Discovery Capital Management",
                     "Discover Financial Services":"Discovery Capital Management",
                     "EquiLe":"Equile",
                     "Ed Rosen of Cleary Gottlieb Steen Hamilton":"Cleary Gottlieb",
                     "ExxonMobil":"Exxon Mobil",
                     "Exxon Mobil Corporation":"Exxon Mobil",
                     "European Fund and Asset Management Association (EFAMA)":"EFAMA",
                     'Extractive Industries\r\r\nTransparency Initiative':"Extractive Industries",
                     "Fidelity Investments":"Fidelity",
                     "Financial Services Roundtable and constituent members":"Financial Services Roundtable",
                     "Financial Services Institute, Inc.":"Financial Services Institute",
                     "GE Capital Corp.":"GE",
                     "GE Capital":"GE",
                     "General Electrc Co.":"General Electric",
                     "Genworth Financial - US Mortgage Insurance":"Genworth Financial",
                     "Sachs":"Goldman Sachs",
                     "State Farm VP Management":"State Farm",
                     "Sachs & Co. and Goldman Sachs Execution & Clearing":"Goldman Sachs",
                     "Goldm":"Goldman Sachs",
                     "Goldman":"Goldman Sachs",
                     "Goldman Sachs Group":"Goldman Sachs",
                     "Gunderson Dettmer Stough Villeneuve Franklin & Hachigi":"Gunderson Dettmer",
                     "General Electrc":"General Electric",
                     "HSBC Global Banking and Markets":"HSBC",
                     "HSBC Securities (USA) Inc.":"HSBC",
                     "HSBC Securities, (USA Inc.":"HSBC",
                     "Hartford Financial Services Group Inc":"Hartford",
                     "ICE Trust and the Intercontinental Exchange":"ICE",
                     "Investent Company Institute":"Investment Company Institute",
                     "Institute of International Bankers (IIB)":"IIB",
                     "Institute of International Bankers":"IIB",
                     "International Swaps and Derivatives Associatio, Inc.":"ISDA",
                     "International Swaps and Derivatives Association (ISDA)":"ISDA",
                     "International Swaps and Derivatives Associatio":"ISDA",
                     "Investment Adviser Association (IAA)":"IAA",
                     "Investment Advisers Associatio":"IAA",
                     "Investment Adviser Associatio":"IAA",
                     "Investment Company Institute and its Members":"Investment Company Institute",
                     "ISLA (International Securities Lending Association)":"ISLA",
                     "ICE Link":"ICE",
                     "ICI (Investment Company Institute)":"ICI",
                     "International banks":"International Banks",
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
                     "Loan Syndications Trading Associatio":"Loan Syndications Trading Association",
                     "MFA":"Managed Funds Associatio",
                     "Managed Funds Association (MFA)":"Managed Funds Associatio",
                     "Markit":"MarkitSERV",
                     "Merrill Lynch, Pierce, Fenner & Smith Inc.":"Bank of America Merrill Lynch",
                     "Metlife":"MetLife",
                     "Millennium Partners":"Millennium",
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
                     "Newedge USA":"Newedge",
                     "National Association of College and University Business Officers (NACUBO)":"NACUBO",
                     "Natural Resources C":"Natural Resources",
                     "Nomur":"Nomura",
                     "Nomura Holding America Inc. and Nomura Securities International":"Nomura",
                     "Nomura Holding America":"Nomura",
                     "Nomura Securities International":"Nomura",
                     "Northern Trust Corporation":"Northern Trust",
                     "Northern Trust Company":"Northern Trust",
                     "North American Securities Administration Associatio":"NASAA",
                     "North American Securities Administrators Associatio, Inc.":"NASAA",
                     'North American Securities Administrators Association ("NASAA")"':"NASAA",
                     "North American Securities Administrators Associatio":"NASAA",
                     "OTC Derivatives Regulators Forum members":"OTC Derivatives Regulators Forum",
                     "Options Clearing Corporation (OCC)":"OCC",
                     "Panel discussion with the Real Estate Investment Securities Associatio":"Real Estate Investment Securities Associatio",
                     "PNC Financial Services Group, Inc.":"PNC",
                     "Pan-Canadian Investors Committee for Third-Party Structured Asset-Backed Commercial Paper":"Pan-Canadian Investors Committee",
                     "PNC Financial Services Group Inc":"PNC",
                     "Principal Financial Group":"Principal",
                     "Property Casualty Association of Americ":"Property Casualty Insurers Association of Americ",
                     "PWYP-US":"PWYP",
                     "Private Equity Growth Company Council":"Private Equity Growth Capital Council",
                     "Promontory Financial Group":"Promontory Financial",
                     "Prudential Financial":"Prudential",
                     "Publish What You Pay":"Publish What You Pay Coalitio",
                     "Putnam Investments Inc":"Putnam",
                     "Putnam  Investments":"Putnam",
                     "RBC Capital Markets":"RBC",
                     "RBC Wealth Management - U.S.":"RBC",
                     "RBC Capital Markets and Sullivan &\r\r\nCromwell":"RBC",
                     "RBS Securities Inc":"RBS",
                     "RBS Americas":"RBS",
                     "RBS Global Banking and Markets":"RBS",
                     "Representatives organized  by the National Association of Manufacturers":"National Association of Manufacturers",
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
                     "Securities Industry and Financial Markets Association (SIFMA) and Davis Polk Wardwell":"SIFMA",
                     "SVB Financial Group":"SVB",
                     "Stable Value Industry Associatio":"Stable Value",
                     "Stable Value Firms":"Stable Value",
                     "Standard and Poors Ratings Services":"Standard Poors Ratings Services",
                     "Swaps Derivatives Market Associatio":"Swaps Derivatives Market Association",
                     "Representatives the Capital Steering Committee of the Securities Industry and Financial Markets Association (SIFMA)":"SIFMA",
                     'TWCMIG"':"TWCMIG",
                     "TD Ameritrade, Inc.":"TD Ameritrade",
                     "Trade repositories (TRs) and ISDA":"ISDA",
                     "Tradeweb":"TradeWeb",
                     "The Clearing House Association":"Clearing House",
                     "The Clearing House Association. Llc":"Clearing House",
                     "The Clearing House Association Llc":"Clearing House",
                     "Tradeweb, LLC":"TradeWeb",
                     "UBS Bank USA":"UBS",
                     "US Chamber of Commerce Center for Capital Markets Competitiveness":"US Chamber of Commerce Center",
                     "US and International Banks":"International Banks",
                     "Wells Fargo Advisors":"Wells Fargo",
                     "Wells Capital Management":"Wells Fargo",
                     "Wells Fargo Securities":"Wells Fargo",
                     "Western Asset Management Co.":"Western Asset Management",
                     "members of SIMFA":"SIFMA",
                     "the Financial Services Roundtable":"Financial Services Roundtable",
                     "Wholesale Markets Brokers?? Associatio":"Wholesale Market Brokers' Associatio",
                     "Dealer members of the Securities Industry and Financial Markets Associatio":"SIFMA",
                     "Rom the Division of Trading and Markets re: Meeting with the Capital Steering Committee of the Securities Industry and Financial Markets Associatio":"SIFMA",
                     "Rom the Division of Trading and Markets re: US Chamber of Commerce":"US Chamber of Commerce",
                     "Rom the Division of Trading and Markets regarding a series of August meetings with Peter Shapiro of Swap Financial Group":"Swap Financial Group",
                     "Yale Endowment":"Yale University",
                     "Yale School of Management":"Yale University",
                     
                     }
        
        if org in formal_name:
#            print("!!!")
            return strip_pron(is_org(formal_name[org]))
        else:
            return strip_pron(is_org(org))
    else:
        return "default"

def strip_comma(inf):
    return inf.strip().strip(";").strip()

def capitalize_first(word):
    if len(word)>1:
        return word[0].upper()+word[1:]
    else:
        return word    
    
non_us_country=["london","european","canada","canadian","british","britian","hong","hk",
         "australia","australian","uk","asian"]
non_us_country=set(non_us_country)
    
stop1=stopwords.words("english")
#len(stop)=179
#stop[0:10]
stop2=["capital","financial","association","association","investment","asset",
       "management","group","industry","security","securities","risk","associ",
       "stor","associatio","manag","firm","forum","union","office","offices","advisor",
       "corporatio","institut","partn","compani","industri","fin","school","counsel",
       "america","gener","japans",'canada','australia',"partner","fund","ventur","capit",
       "nation","univers","consult","offic","union","labor","bank","staff","repres","member",
       "author","secur","financi","roundtabl","fix","incom","intern","hk"]
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

def stem_org(org):
    org=org.lower()
    org=" ".join([porter_stemmer.stem(i) for i in org.split()])
    org=remove_stop_words(org,stop)
    org=strip_pron(org)
    return org

def remove_punc(word, punc):
    for i in punc:
        if i in word:
            ind=word.find(i)
            word=word[:ind]+word[ind+1:]
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

def same_country(org,Org):
    org_l=[porter_stemmer.stem(w).lower() for w in org.split()]
    Org_l=[porter_stemmer.stem(w).lower() for w in Org.split()] 
    for c in non_us_country:
        if c in org_l:
            if c not in Org_l:
                return 0
        else:
            if c in Org_l:
                return 0
    return 1

def acc_partial_score(org, Org, stop):
#    accept=0
    count_o=0
    count_O=0
    org_l=[porter_stemmer.stem(w) for w in org.split()]
    Org_l=[porter_stemmer.stem(w) for w in Org.split()]    
    for w in org_l:
        if w not in Org_l:#"Yale University" "Yale"; "goldman" "goldman sachs" 
            return -1
        
    for word in org_l:
        if word in stop:
            count_o+=1
    for word in Org_l:
        if word in stop:
            count_O+=1
    if len(org_l)-count_o == len(Org_l)-count_O:
        return 1
    else:
        return 0
    
def contain_barcket_or_upper(word):#use for find abb
    if "(" in word and ")" in word:
        word_p=word[word.find("(")+1:word.find(")")]
        if porter_stemmer.stem(word_p) not in stop:
            return word_p.upper().strip()
        else:
            word=word[:word.find("(")]+word[word.find(")")+1:]
            word=word.replace("  "," ")
    for w in word.split():
        if is_abb(w):
            if porter_stemmer.stem(w).lower() not in non_us_country:
                return w
    return word
    
def abbize(org,stop):
    return "".join([i[0].upper() for i in org.split() if i not in stop])
        
    
threshold=50
def match_org(org, Org_l,threshold):
    org=contain_barcket_or_upper(org)
    score=0
    score2=0
    part_score=0
    org_mat="individual"
    org_stem=stem_org(org)
    try2=0
    org_abb=abbize(org,stop1)
    if len(org_stem.split())==1:
        try2=1
        org_stem=org_stem.upper() 
    
    
    
    for Org in Org_l:
        
        if is_abb(Org):
            if ratio_abbreviation(org,Org)==100 or try2*ratio_abbreviation(org_stem,Org)==100 or org_abb==Org:
                return [1,Org]
        else:
            part_score_t=fuzz.partial_ratio(stem_org(org),stem_org(Org))#should figure out a way to deal with 100 score. if org has some of the words not in stop, and is part of org dic \if some else words not in stop, then has problem 
            acc_p=0
            if part_score_t==100:
                acc_p=acc_partial_score(org, Org, stop)
                if acc_p==1:
                    return [1, Org]
                else:
                    pass
            score_t=fuzz.ratio(stem_org(org),stem_org(Org))
            score2_t=fuzz.ratio(org,Org)
            counrty_ind=same_country(org,Org)
            if part_score_t >= 81 and score_t>=threshold and acc_p!=-1 and counrty_ind:
            
                if score2_t>=score2:
                    score=score_t
                    part_score=part_score_t
                    score2=score2_t
                    org_mat=Org
    if part_score >= 81 and score>=threshold and score2>=60:
        return [1, org_mat]
    else:
        return [0,"Individual"]











def redeal_filename(name):
    name=name.replace(".","_")
    name=name.replace("_&","")
    name=name.replace("__","_")
    return name
    
def find_len(s):
    r='[a-zA-Z0-9]+'
    ws = re.findall(r,s)
    l=len(ws)
    return l

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


save_pickle_add2=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_meeting_small_rule.pickle"
#pickle.dump(SEC_meeting_all, open(save_pickle_add2,"wb"))
with open(save_pickle_add2,"rb") as f:
    tem=pickle.load(f, encoding='latin1')
dataframe_meeting=tem
org_set=dataframe_meeting["organization"].unique()
#for i in dataframe_meeting["organization"].unique():
#    print(i)


stem_word_in_org=set()
stop_add=[]
for words in org_set:
    word_l=words.split()
    for word in word_l:
        candi=porter_stemmer.stem(word).lower()
        if candi not in stop:
            if candi in stem_word_in_org:
                stop_add.append(candi)
            else:
                stem_word_in_org=stem_word_in_org|set([candi])

too_frequent=["a","admiinistr","afric","africa","bar","best","buy",
              "better","broker","commissio","commission","common",
              "congress","econom","entiti","exchang","first","global",
              "implement","leader","london","micro","new","p","pay","resourc",
              "research","york","one","franc","french","polici","structur",
              "notebook","underwrit","delta","foreign","loan","personal",
              "natur","relat","growth","borrow","meet","organ","benefit",
              'practic','strategi']
too_fre_set=set(too_frequent)
stop=stop1+stop2+stop_add
stop=set(stop)
org_dic={}
org_words_set=[]
for words in org_set:
    word_l=words.split()
#    ind=0
    for word in word_l:
        candi=porter_stemmer.stem(word).lower()
        org_words_set.append(candi)
        if candi not in stop and candi not in too_fre_set:
            org_dic[candi]=words
#            ind=1
        
org_words_set=set(org_words_set)
o=list(org_words_set)
o.sort()

punctuation=list(string.punctuation)
punctuation.remove("&")
punctuation.remove("/")
punctuation.remove("(")
punctuation.remove(")")



path_basic=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\final rule\SEC_rule\final"
path=path_basic+"\\10.pdf"
raw_S,npag=pdf_parse1(path)
##path_save=path_basic+"\\final_rule_banking_1.txt"
##with open(path_save, 'w') as f:
##    f.write(str(S))
##len(S.split())
#
#S=raw_S.replace("\n"," ").replace("'"," ").replace("\\"," ")
##S=" ".join([strip_pron(i) for i in S.split() if i not in punctuation])#since we replace "&" by " ", it's better to return a string not a list
#S=" ".join([strip_pron(i) for i in S.split()])
#word_in_S=S.split()
#Voc=""
#continuous_ind=""
#for word in word_in_S:
#    if porter_stemmer.stem(word).lower() in org_words_set:
#        Voc+=continuous_ind
#        Voc+=word
#        Voc+=" "
#        continuous_ind=""
#    else:
#        continuous_ind="1 "
#
#if Voc[0]=="1":
#    Voc=Voc[2:]
#word_in_S_n=Voc.split(" 1 ")
#
#
#org_citation={}
#for org in org_set:
#    org_citation[org]=0
#
#not_match_word=[]
#for word in word_in_S_n:
#    spl_word=word.split()
#    find_org_ind=0
#    tem_org=""
#    for s_word in spl_word:
#        stem_word=porter_stemmer.stem(s_word).lower()
#        if stem_word in org_dic:
#            org_find=org_dic[stem_word]
#            if org_find != tem_org:
#                org_citation[org_find]+=1
#                find_org_ind=1
#                tem_org=org_find
#    if find_org_ind==0:
#        possi_Cov=[]
#        for voc_i in range(1,min(7, len(spl_word))):
##            Voc.append([])
##            tem=""
#            for i in range(len(spl_word)-voc_i):
#                tem=" ".join(word_in_S[i:i+voc_i])
##                Voc[-1].append(rewrite_orgname(tem))
#                rt=rewrite_orgname(tem)
#                at=abbize(tem,stop1)
#                if rt in org_set:
#                    org_citation[rt]+=1
#                elif at in org_set:
#                    org_citation[at]+=1
#                else:
#                    pass
#                    
#            
#
##volcker rule: 1, 10
#citation_result_list=[]
#for org in org_citation.keys():
#    citation_result_list.append({})
#    citation_result_list[-1]["organization"]=org
#    citation_result_list[-1]["citation"]=org_citation[org]
##    citation_result_list[-1]["rule type"]=rule_type
#    citation_result_list[-1]["rule type number"]=1
#    
#save_pickle_add_v=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_citation"+str(1)+".pickle"
##pickle.dump(citation_result_list, open(save_pickle_add_v,"wb"))   




#for voc_i in range(1,8):
#    Voc.append([])
#    tem=""
#    for i in range(len(word_in_S)-voc_i):
#        tem=" ".join(word_in_S[i:i+voc_i])
#        Voc[-1].append(rewrite_orgname(tem))
#        
#
#        
#org_citation={}
#for org in org_set:
#    org_citation[org]=0
#    
#for voc_i in range(0,7):
#    for word in Voc[voc_i]:
#        if word in org_set:
#            org_citation[word]+=1
        

#first deal with orginzation set we have in SEC meetings
#stem them and remove the stop words,leave only unique word
#for org that has a lot of stop words, leave them completely

#first see whether the word in org happens twice, if so, add them to the stop words
#so all the org's word that has not been removed can uniquely represent the org
#and creates an dic

#then, for 


#then stem the word in final rule
#leave the words that are not in the unique org set
#keep the word that has more than one upper word
#compare them with the org set, if continuous two belong to the same org,
#then add only once





#final_rule_good=[0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]
final_rule_good=[10]

for i_large in range(0,len(final_rule_good)):
    read_rule_num=final_rule_good[i_large]
    print(read_rule_num)
    path_basic=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\final rule\SEC_rule\final"
    path=path_basic+"\\"+str(read_rule_num)+".pdf"
    S,npag=pdf_parse1(path)
    #path_save=path_basic+"\\final_rule_banking_1.txt"
    #with open(path_save, 'w') as f:
    #    f.write(str(S))
    #len(S.split())
    
    S=S.replace("\n"," ").replace("'"," ").replace("\\"," ")
    #S=" ".join([strip_pron(i) for i in S.split() if i not in punctuation])#since we replace "&" by " ", it's better to return a string not a list
    S=" ".join([strip_pron(i) for i in S.split()])
    word_in_S=S.split()
    Voc=""
    continuous_ind=""
    for word in word_in_S:
        if porter_stemmer.stem(word).lower() in org_words_set:
            Voc+=continuous_ind
            Voc+=word
            Voc+=" "
            continuous_ind=""
        else:
            continuous_ind="1 "
    
    if Voc[0]=="1":
        Voc=Voc[2:]
    word_in_S_n=Voc.split(" 1 ")
    
    
    org_citation={}
    for org in org_set:
        org_citation[org]=0
    
    not_match_word=[]
    for word in word_in_S_n:
        spl_word=word.split()
        find_org_ind=0
        tem_org=""
        for s_word in spl_word:
            stem_word=porter_stemmer.stem(s_word).lower()
            if stem_word in org_dic:
                org_find=org_dic[stem_word]
                if org_find != tem_org:
                    org_citation[org_find]+=1
                    find_org_ind=1
                    tem_org=org_find
        if find_org_ind==0:
            possi_Cov=[]
            for voc_i in range(1,min(7, len(spl_word))):
    #            Voc.append([])
    #            tem=""
                for i in range(len(spl_word)-voc_i):
                    tem=" ".join(word_in_S[i:i+voc_i])
    #                Voc[-1].append(rewrite_orgname(tem))
                    rt=rewrite_orgname(tem)
                    at=abbize(tem,stop1)
                    if rt in org_set:
                        org_citation[rt]+=1
                    elif at in org_set:
                        org_citation[at]+=1
                    else:
                        pass
                        
                
    
    #volcker rule: 1, 10
    citation_result_list=[]
    for org in org_citation.keys():
        citation_result_list.append({})
        citation_result_list[-1]["organization"]=org
        citation_result_list[-1]["citation"]=org_citation[org]
    #    citation_result_list[-1]["rule type"]=rule_type
        citation_result_list[-1]["rule type number"]=read_rule_num
        
    save_pickle_add_i=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_citation"+str(read_rule_num)+".pickle"
    pickle.dump(citation_result_list, open(save_pickle_add_i,"wb"))   
    

with open(save_pickle_add_i,"rb") as f:
    tem=pickle.load(f, encoding='latin1')




    
    
    
    
    
    
    
    
    
    
    



        
        
        