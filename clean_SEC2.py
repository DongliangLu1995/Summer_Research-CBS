# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 00:28:21 2019

@author: DongliangLu
"""

#clean the comments and download
# -*- coding: utf-8 -*-

import pandas as pd
import re
import pickle
import numpy as np
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import nltk
import string
import requests
import os
from bs4 import BeautifulSoup

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
import PyPDF2


#pdf_url="https://www.sec.gov/comments/df-title-ii/bd-liquidation/bdliquidation-26.pdf"
#pdf_url="https://www.sec.gov/comments/df-title-ii/bd-liquidation/bdliquidation-25.htm"
#
#pdf_url="https://www.sec.gov/comments/df-title-ii/bd-liquidation/bdliquidation-15.htm"
#
#save_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\download\SEC_comments\rule_0"
#
#if pdf_url.endswith(".pdf"):
#    pdf_save_add=save_add+"\\"+"comments_"+str(0)+".pdf"
#    get_pdf_comments(pdf_url,pdf_save_add)
#else:
#    htm_save_add=save_add+"\\"+"comments_"+str(0)+".txt"
#    get_htm_comments(pdf_url,htm_save_add)
#
#
#def get_pdf_comments(pdf_url,pdf_save_add):
#    r=requests.get(pdf_url)
#    with open(pdf_save_add,"wb") as f:
#        f.write(r.content)
#    print("saving pdf for rule "+str(0)+" done")
#        
#def get_htm_comments(htm_url,htm_save_add):
#    soup=BeautifulSoup(requests.get(htm_url).text,"lxml")
#    P=soup.find_all("p")
#    A=soup.find_all("a")
#    if not A:
#        text=""
#        for p in P:
#            text+=p.text
#            text+="\n\n"
#        with open(htm_save_add,"w") as f:
#            f.write(text)
#        print("saving pdf for rule "+str(0)+" done")    
#    else:
#        for href in A:
#            comment_url="https://www.sec.gov"+A[0]['href']
#            r=requests.get(comment_url)
#            with open(pdf_save_add,"wb") as f:
#                f.write(r.content)
#
#
#
#t=pdf_parse1(pdf_save_add)
#text=t[0]
#t=pdf_parse2(pdf_save_add)
#text=t[0]
#    
#pdf_url="https://www.sec.gov/comments/df-title-ii/bd-liquidation/bdliquidation-15b.pdf"
# 
#    
#u_pattern=re.compile(b"\\u\d+")
#re.findall(u_pattern, text)    
#    
#save_add2=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\download\SEC_comments\rule_0\comments_0.txt"
#save_add3=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\download\SEC_comments\rule_0"+"\\Credit Roundtable and Fixed Income Forum_1.pdf"
#pdf_parse1(save_add3)
#t=pdf_parse2(save_add3)
#text=t[0]
#
#text=text.encode('latin-1', 'replace').decode("utf-8","ignore").replace("?"," ")
#
#save_add4=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\download\SEC_comments\rule_0"+"\\Credit Roundtable and Fixed Income Forum_1.txt"
#with open(save_add4,"w") as f:
#    f.write(text)
#
#encoding="latin-1"
#with open(save_add2,"w",encoding="latin-1") as f:
#    f.write(text)
#    
#with open(save_add2,encoding="UTF-8") as f:
#    f.write(text)
#
#encoding="ascii", errors="surrogateescape"
#with open(htm_save_add,encoding="ascii", errors="surrogateescape") as f:
#    f.write(text)








data_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"
SEC_comments_data=pd.read_csv(data_add+"\\SEC_comments.csv",index_col=0)

org_pickle=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_meeting_total.pickle"
with open(org_pickle,"rb") as f:
    tem=pickle.load(f, encoding='latin1')

org_clean=set(tem.keys())

new_org=["Prudential","Renaissance","Putnam","American Express",
         "Japanese Bankers Assocation","Invesco","CalPERS","Vanguard",
         "CIEBA","FTN","FSA","NACL","NAMIC","UKRCBC","TCW","BBVA","Western Asset Management",
         "Union Asset",]
new_org=set(new_org)
org_clean=org_clean|new_org
org_for_see=list(org_clean)
org_for_see.sort()


non_us_country=["london","european","canada","canadian","british","britian","hong","hk",
         "australia","australian","uk","asian"]
non_us_country=set(non_us_country)


stop1=stopwords.words("english")

stop2=["capital","financial","association","association","investment","asset",
       "management","group","industry","security","securities","risk","associ",
       "stor","associatio","manag","firm","forum","union","office","offices","advisor",
       "corporatio","institut","partn","compani","industri","fin","school","counsel",
       "america","gener","japans",'canada','australia',"partner","fund","ventur","capit",
       "nation","univers","consult","offic","union","labor","bank","staff","repres","member",
       "author","secur","financi","roundtabl","fix","incom","intern","hk","administr",
       "advisori","global","Union Asset"]
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
    not_org=["&",
            "Wu",
             "Advisory",
             "As You Sow",
             "Change to Wi",
             "Consulting",
             "Free the Slaves",
             "Friends of the Congo",
             "Jr.",
             "LCH.Clearnet and Rich Feuer Group",
             "Lt",
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
             "U.S. Insurer",
             "Congress Watch/Public Citize",
             "Rom the Division of Trading and Markets regarding an article submitted by George Friedm",
             "And Labaton Sucharow",
             "",
             'Other organizations',
             'Other unions',
             "US",
             'County',
             'Europe',
             'Economic',
             'Examinations',
             'Markets',
             'Poors',
             'r',
             'America',
             'Americ',
             'Company',
             'City of New York',
             'Chair',
             'FINANCIAL',
             'Rulemaking',
             'S well as Susan Voss',
             'Members',
             'New York City',
             'New Engl',
             'Poor',
             'Responsible',
             'Research',
             'the'
            ]
    if org in not_org or org.startswith("certain") or len(org)<=1:
        return "Individual"
    else:
        return org
    #start with certain
    
def sepe_and(org):
    and_comp=["DBRS and Pickard Djinis",
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
              "RBC Capital Markets and Sullivan Cromwell LLP",
              "SVB Financial Group and Debevoise Plimpton LLP",
              "State Farm and Arnold Porter",
              "The Depository Trust Clearing Corporatio",
              "Wells Fargo Advisors and First Clearing, LLC",
              "AFSCME and AFL-CIO",
              "American Benefits Council and CIEBA",
              "Assured Guaranty and the Association of Financial Guaranty Insurers",
              "Citadel LLC and Delta Strategy Group",
              "Citadel LLC and Winston Strawn",
              "Institute of International Bankers and Cleary Gottlieb Steen Hamilton",
              "Loan Syndications Trading Association and WilmerHale",
              "SVB Financial Group and Debevoise Plimpton",
              "Wells Fargo Advisors and First Clearing",
              "National Venture Capital Association and Proskauer Rose",
              "Trade repositories (TRs) and ISDA",
              "Service Employees International Union; American Federation of State",
              "Calvert Asset Management and Social Investment Forum",
              "Citadel LLC and Winston Strawn",
              "County and Municipal Employees; Council of Institutional Investors; Consumer Federation of America; and Labaton Sucharow",
              "ICE Inc and Creditex",
              "LCHClearnet and Rich Feuer Group",
              "Grohovsky Whipple; Vogel",
              "Staff of Senator Jeff Merkley and Senator Carl Levi",
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
    if "'s" in org:
        org = org.replace("'s",'')
    pron=[",","'","."]
    if "&" in org:
        org = " ".join([i.strip() for i in org.split("&")])
    if "/" in org:
        org = " ".join([i.strip() for i in org.split("/")])
    for p in pron:
        if p in org:
            org=org.replace(p,"")
    if org.find('Rom ')==0:
        org = org[4:]
    return org

def strip_staff(org):
    #staff and company title
    if "Investment Company Institute" in org:
        org = org.replace("Investment Company Institute", "ICI")
    staff_list = ["Committee of", "Committee on","Committee from",
                  "Staff of","Staff from","Staff on", "Committees",
                  'Office of','Division of','Institute of','Board of','Representative']
    company_title_list = ['Financial Service','Insurance Company','Corporation',
                          'Corp','Finance','Insurance Companies',
                          'Investments','Investment Group','Investment Management Research',
                          'Investment Management','Investors Management','Investors Service',
                          'Investment','Global Markets','Group','Company',
                          'Ltd','Holdings','Funds','Fund',
                          'St', 'Financial Services','Capital Management',
                          'Holding','Asset Management','Associates','Capital Advisors',
                          'Capital','Derivative Markets','Derivatives Markets',
                          'Limite','Trust','Partners','Securities','Services',
                          'representatives','Management','Management Research',
                          'Technologies','Coalitio','coalitio',
                          
                          ]
#    company_title_pattern = re.compile("\ "+"("+"|".join(company_title_list)+")"+"$")
    company_title_pattern = re.compile("("+"|".join(company_title_list)+")"+"$")
    for staff in staff_list:
        org = org.replace(staff,"")
    for title in company_title_list:
        org = company_title_pattern.sub("", org)
    if org.find('of ') == 0:
        org = org[2:]
    of_pattern = re.compile('of$')
    org = of_pattern.sub('',org)
    return org.strip()


def strip_bad_format(org):
    start_format_list = ['with ','behalf of ','epresentatives of ','Representing ',
                         'Rom ','S ','S well as ','office of']
    end_format_list = [' regarding',' of Amer']
    start_pattern = re.compile("("+"|".join(start_format_list )+")")
    end_pattern = re.compile("("+"|".join(end_format_list)+")")
    if start_pattern.search(org):
        org = org[start_pattern.search(org).span()[1]:]
    if start_pattern.search(org):
        org = org[start_pattern.search(org).span()[1]:]
    if end_pattern.search(org):
        org = org[:end_pattern.search(org).span()[0]]
    return org



def tio_to_tion(org):
    org_l=org.split()
    if "Associatio" in org_l:
        org_l[org_l.index("Associatio")]="Association"
    if "Corporatio" in org_l:
        org_l[org_l.index("Corporatio")]="Corporation"
    return " ".join(org_l)

def contain_abb(org):
    org_split = org.split()
    if len(org_split)>1:
#        for org_s in org_split[:-1]:
        for org_s in org_split[:1]:#only consider the first word
            if org_s == org_s.upper() and len(org_s)>1 and org_s != 'US':
                return 1,org_s
        return 0,org
    else:
        for org_s in org_split:
            if org_s == org_s.upper() and len(org_s)>1:
                return 1,org_s
        return 0,org




def rewrite_orgname(org):
    org = org.replace("-","")
    org = strip_pron(org)
    org = strip_staff(org)
   
    
    bracket_pattern = re.compile("\(.*\)")
    if bracket_pattern.findall(org):
        tem = bracket_pattern.findall(org)[0][1:-1].strip().upper().strip('"').strip('"')
        if tem != 'US':
            return bracket_pattern.findall(org)[0][1:-1].strip().upper().strip('"').strip('"')
        else:
            org = org.replace("(US)","")
            org = org.replace('(US )',"")
            
    
    contain_abb_or_not,org = contain_abb(org)
    if contain_abb_or_not:
        return strip_pron(org).strip(")").strip("(")
    
    
    strip_list=["Inc","Inc.","LP","L.P.","Co","Co.","LLP","& Co.",", Inc.","LLC","Corp.","&",","]
    
        
    if type(org)==str:
        t_pattern=re.compile("[Tt]he ")
        #don't use replace directly, or it will be some problem
        if re.match(t_pattern,org):
            org=org[4:]
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

        formal_name={"American Bakers' Association": "ABA",
                     "American bakers' association":"ABA",
                     "American Bankers Association":"ABA",
                     "American Bankers' Association":"ABA",
                     'American Bar Association':'ABA',
                     "American for Financial Reform":"AFR",
                     "Americans for Financial Reform":"AFR",
                     'American Academy of Actuaries':'AAA',
                     "American Society of Farm Managers":'ASFM',
                     "American Society of Corporate Secretaries":'ASCS',
                     "American Society of Appraisers":'ASA',
                     'American Automotive Leasing Association':'AALA',
                     "American Institute of Certified Public Accountants":'AICPA',
                     "ABASA":"ABA",
                     "Caleb Gibson of Americans for Financial Reform":"AFR ",
                     "Ameriprise Financial":"Ameriprise",
                     "American Council of Life Insurers":"ACLI",
                     "Alternative Investment Management Association (AIMA)":"AIMA",
                     "Alternative Investment Management Associatio":"Alternative Investment Management Association",
                     "Alternative Investment Management Association":"AIMA",
                     "Air Transportation Association":"ATA",
                     "Advanced Practice Advisors":"APA",
                     "Advance Micro Devices":'AMD',
                     "Asset Management Association":"AMA",
                     "American Benefits Council":"ABC",
                     "American Equity Investment Life":"American Equity",
                     "American Equity Life":"American Equity",
                     "American Petroleum Institute (API)":"API",
                     "American Petroleum Institute":"API",
                     "AFL-CIO Office of Investment":"AFLCIO",
                     "American Federation of Labor and Congress of Industrial Organizations":"AFLCIO",
                     "AFL-CIO":"AFLCIO",
                     "AFSCME Capital Strategies":"AFSCME",
                     "Australian Securitisation Forum":"ASF",
                     "American Federation of State":"AFS",
                     "American Public Gas Association":"APGA",
                     "Andrew Green from the Office of US Senator Jeff Merkley":"Jeff Merkley",
                     "AVX Corporation":"AVX",
                     "AVX Corporatio":"AVX",
                     "Association for Advanced Life Underwriting":"AALU",
                     "Association for Financial Professionals":"AFP",
                     "Association of Financial Guaranty Insurers":"AFGI",
                     "Association of Institutional Investors":"AII",
                     'Association of Mortgage Investors':'AMI',
                     'Association of Private French Enterprises':'APFE',
                     'Asbill Bre':'Asbill Brennan',
                     'Asbil Bre':'Asbill Brennan',
                     'Asbil Brennan':'Asbill Brennan',
                     "BB&T Capital Markets":"BBT",
                     "BB&T Corporation":"BBT",
                     "BB T":"BBT",
                     'American Securitization Forum':'ASF',
                     "BMO Harris Bank N.A.":"BMO",
                     "BMO Financial Corp.":"BMO",
                     "BMO Financial":"BMO",
                     "BNY Mellon Corporation":"BNY Mellon",
                     "Bank Of New York Mellon":"BNY Mellon",
                     "BNY Mellon Clearing":"BNY Mellon",
                     "BNY/Mello":"BNY Mellon",
                     "BNY/Mell":"BNY Mellon",
                     "Bank of New York Mellon Corp.":"BNY Mellon",
                     "Bank of New York Mellon":"BNY Mellon",
                     "Bank of New York Mello":"BNY Mellon",
                     "Bank Of New York Mellon":"BNY Mellon",
                     "Bank Of New York Mello":"BNY Mellon",
                     "Bank of Americ":"Bank of America Merrill Lynch",
                     "BoA":"Bank of America Merrill Lynch",
                     "BAC":"Bank of America Merrill Lynch",
                     "Bank of America":"Bank of America Merrill Lynch",
                     "Bank of America and Merrill Lynch":"Bank of America Merrill Lynch",
                     "Barclays Capital":"Barclays",
                     "Barclays Capital":"Barclays",
                     "BBVA Compass Consulting and Benefits":"BBVA",
                     "Better Markets":"Better Markets",
                     "Best Buy":"Best Buy",
                     "BNY ConvergEx Group":"BNY Mellon",
                     "BP p.l.c.":"BP",
                     "BHP Billiton Ltd.":"BHP Billiton",
                     "BlackRock Inc.":"BlackRock",
                     "Blackrock":"BlackRock",
                     "Bloomberg L.P.":"Bloomberg",
                     "Bloomberg LP":"Bloomberg",
                     "BlueMountain Capital Management":"BlueMountain",
                     "Board of Directors of the Bond Dealers of America":"BDA",
                     "Bond Dealers of Americ":"BDA",
                     "Bond Dealers of America":"BDA",
                     "Board of Directors of the Bond Dealers of Americ":"Board of Directors of the Bond Dealers of America",
                     "Boston Common Asset Management":"BCAM",
                     "British Bankers Association":"BBA",
                     "Boston University School of Law":"Boston University",
                     "Broadridge Financial Solutions":"Broadridge",
                     "Capstone LLC":"Capstone",
                     "Calvert Asset Management":"Calvert",
                     "Calvert Investments":"Calvert",
                     'Canadian Bankers Association':'CBA',
                     "California Public Employees' Retirement System":"CalPERS",
                     "California Public Employees Retirement System":"CalPERS",
                     "California State Teachers Retirement System":"CalPERS",
                     "Canadian Banks and the Canadian Bankers?? Associatio":"Canadian Banks and the Canadian Bankers Association",
                     'Canadian Banks and the Canadian Bankers\x92 Association':"Canadian Banks and the Canadian Bankers Association",
                     "Canadian Banks and the Canadian Bankers Associatio":"Canadian Banks and the Canadian Bankers Association",
                     "Canadian Securities Administrators":"CSA",
                     'Center for Capital Markets Competitiveness event on "Over the Counter (OTC) Derivatives Reform: Preparing for a Changing Marketplace"':'Center for Capital Markets Competitiveness',
                     "Certified Financial Planner Board of Standards":"CFP",
                     "CFA Inst":"CFA",
                     "CFTC and certain pension plans":"CFTC",
                     "CRE Finance Council":"CRE",
                     "Center for Study of Financial Market Evolution (CSFME)":"CSFME",
                     'Center for American Progress Actio':'CAP',
                     'Center for American Progress Action':'CAP',
                     "Conference call CRE Finance Council":"CRE",
                     'Center for Responsible Lending':'CRL',
                     'Center for Capital Markets Competitiveness':'CCMC',
                     "Citi":"Citigroup",
                     "Citigroup Inc":"Citigroup",
                     "Citibank":"Citigroup",
                     "citibank":"Citigroup",
                     "Clearly":"Cleary Gottlieb",
                     "Cleary":"Cleary Gottlieb",
                     "Clearly Gottlieb Steen Hamilto":"Cleary Gottlieb",
                     'Clearly Goottlieb Steen Hamilton':"Cleary Gottlieb",
                     "Clearly Gottlieb":"Cleary Gottlieb",
                     "Cleary Gottlieb Steen Hamilton":"Cleary Gottlieb",
                     "Chicago Mercantile Exchange Group":"CME",
                     "Cleary Gottlieb Steen Hamilto":"Cleary Gottlieb",
                     "Cleary Gottlieb & Steen Hamilto":"Cleary Gottlieb",
                     "Cleary Gottlieb and Steen Hamilto":"Cleary Gottlieb",
                     "Cleary Gottlieb and Steen Hamilton":"Cleary Gottlieb",
                     'Chicago Board Options Exchange':'CBOE',
                     'Commercial Mortgage Securities Association':'CMSA',
                     'Consumer Mortgage Coalitio':'CMC',
                     'Commercial Real Estate Finance Council':'CREFC',
                     'Commercial Mortgage Securities Association':'CMSA',
                     "Council of Institutional Investors":"CII",
                     "Committee for the Fiduciary Standar":"Fiduciary Standar",
                     "Committee of Annuity Insurers regarding Business Conduct Standards":"Annuity Insurers",
                     "Commodity Futures Trading Commissio":"CFTC",
                     'Committee on Investment of Employee Benefit Assets\r\r\n(CIEBA)':"CIEBA",
                     'Conference of State Bank Supervisors ("CSBS")':"CSBS",
                     "Clients and the law firm of Gibso":"Gibso",
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
                     "CFP Boar":"CFP",
                     "Fixed Income Forum and Credit Roundtable":"Credit Roundtable Fixed Income Forum",
                     "Credit Roundtable and Fixed Income Forum":"Credit Roundtable Fixed Income Forum",
                     "Davis Polk":"Davis Polk Wardwell",
                     "Davis Polk and Wardwell":"Davis Polk Wardwell",
                     "Davis, Polk & Wardwell":"Davis Polk Wardwell",
                     "Davis Polk & Wardwell LLP":"Davis Polk Wardwell",
                     "Debevoise":"Debevoise Plimpton",
                     "Debevoise &amp":"Debevoise & Plimpton",
                     "Depository Trust & Clearing Corporatio":"Depository Trust Clearing",
                     "Depository Trust Clearing Corporation":"Depository Trust Clearing",
                     "Deutsche Bank AG New York":"Deutsche Bank",
                     "Deutsche Bank Americas":"Deutsche Bank",
                     "Deutsche Bank Americas Corp.":"Deutsche Bank",
                     "Deutsche Bank and Sidley Austi":"Deutsche Bank",
                     'Deloitte Touche':'Deloitte',
                     'Depository Trust Clearing':'Depository Trust',
                     'Depository Trust Clearing Group':'Depository Trust',
                     "D. E. Shaw & Co., LLP":"DE Shaw",
                     "D. E. Shaw":"DE Shaw",
                     "D.E. Shaw":"DE Shaw",
                     "D E Shaw":"DE Shaw",
                     "DE":"DE Shaw",
                     "Deckert":"Dechert",
                     "Dealer members of the Securities Industry and Financial Markets Association":"SIFMA",
                     "Depository Trust and Clearing Corporatio":"Depository Trust Clearing",
                     "Depository Trust Clearing Corporation":"Depository Trust Clearing",
                     "Discovery":"Discovery Capital Management",
                     "Discover Financial Services":"Discovery Capital Management",
                     "EquiLe":"Equile",
                     "Ed Rosen of Cleary Gottlieb Steen Hamilton":"Cleary Gottlieb",
                     "ExxonMobil":"Exxon Mobil",
                     "Exxon Mobil Corporation":"Exxon Mobil",
                     'Education Finance Council':'EFC',
                     'Equity Growth Capital Council':'EGCC',
                     "European Fund and Asset Management Association (EFAMA)":"EFAMA",
                     "ERISA-Regulated Pension Plans":"ERISA",
                     'Extractive Industries\r\r\nTransparency Initiative':"EITI",                     
                     "Extractive Industries Transparency Initiative":"EITI",
                     "Fidelity Investments":"Fidelity",
                     "Financial Services Roundtable and constituent members":"FSR",
                     "Financial Services Institute, Inc.":"FSI",
                     "Financial Industry Regulatory Authority":"FINRA",
                     "Financial Planning Association":"FPA",
                     "Financial Planning Coalitio":"FPC",
                     "Financial Services Forum":"FSF",
                     "Financial Services Institute":"FSI",
                     "Financial Services Roundtable":"FSR",
                     "FTN Financial Capital Markets":"FTN",
                     "Fixed Income Forum Credit Roundtable":"Credit Roundtable Fixed Income Forum",
                     "Forum for Sustainable and Responsible Investment":"FSR",
                     "GE Capital Corp.":"GE",
                     "GE Capital":"GE",
                     "Gibson Dunn and Crutcher":"Gibson Dunn",
                     "Gibso":"Gibson Dunn",
                     "Gibson":"Gibson Dunn",
                     "Dunn and Crutcher":"Gibson Dunn",
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
                     "HSBC Life":"HSBC",
                     "Hartford Financial Services Group Inc":"Hartford",
                     "Housing and Urban Affairs":"HUA",
                     "ICE Trust and the Intercontinental Exchange":"ICE",
                     "Investent Company Institute":"Investment Company Institute",
                     "Institute of International Bankers (IIB)":"IIB",
                     "Institute of International Bankers":"IIB",
                     "Institute of International Finance":"IIF",
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
                     "ICI Global":"ICI",
                     "ICI Invesco":"ICI",
                     "International banks":"IIB",
                     "ICI Flynn Fusselman":"ICI",
                     "ICI Alfred Brock":"ICI",
                     "Alfred Brock":"ICI",
                     'Industry and Financial Markets Association ("SIFMA")':"SIFMA",
                     "International Swaps":"ISDA",
                     "IIB and EBF":"IIB",
                     "International Banks":"IIB",
                     "Information Technology Industry Council":"ITIC",
                     "Institute for the Fiduciary Standar":"IFS",
                     "International Swaps and Derivatives Association":"ISDA",
                     "International Swaps and Derivatives Association and the Securities Industry and Financial Markets Association":"ISDA",
                     "JC Penney Company":"JC Penney",
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
                     "JPMC":"J.P. Morgan",
                     "JP":"J.P. Morgan",
                     "Jefferies & Company":"Jefferies",
                     "Jewelers of Americ":"JA",
                     "LLP; and Kenney & McCafferty":"Kenney & McCafferty",
                     "Laborers?? International Union of North Americ":"International Union of North America",
                     'Laborers\x92 International Union of North Americ':"International Union of North America",
                     "Labor Union Representatives":"Labor Union",
                     "Law office of Baker":"Baker",
                     "Levin and 			Markey":"Levin Institute",
                     "LCHClearnet":"LCH",
                     "Loomis, Sayles":"Loomis Sayles",
                     "Loomis, Sayles  L.P.":"Loomis Sayles",
                     "Loan Syndications Trading Associatio":"LSTA",
                     "Loan Syndications Trading Association":"LSTA",
                     "London Financial Services Authority":"LFSA",
                     "Manufacturing Jewelers Suppliers of Americ":"NJSA",
                     "Managed Funds Associatio":"MFA",
                     "Managed Funds Association (MFA)":"MFA",
                     "Managed Funds Association":"MFA",
                     "Massachusetts Educational Financing Authority":"MEFA",
                     "Members and the National Venture Capital Association":"NVCA",
                     "Member of Congress":"Congress",
                     "Markit":"MarkitSERV",
                     "Merrill Lynch, Pierce, Fenner & Smith Inc.":"Bank of America Merrill Lynch",
                     "Metlife":"MetLife",
                     "Millennium Partners":"Millennium",
                     "Morgan Stanley Smith Barney":"Morgan Stanley",
                     "Motorola Solutions":"Motorol",
                     "Motorol, Inc.":"Motorol",
                     'Moodys':'Moody',
                     "Municipal Securities Rulemaking Boar":"MSRB",
                     "Mortgage Insurance Companies of Americ":"MICA",
                     "National Association of Mutual Insurance Companies":"NAMIC",
                     "National Association of industrial Bankers":"NAIB",
                     "National Association of Industrial Bankers":"NAIB",
                     'National Association of Insurance Commissioners ("NAIC")':"NAIC",
                     "National Association of Insurance Commissioners (NAIC)":"NAIC",
                     "National Association of Insurance Commissioners":"NAIC",
                     'National Association of Insurance and Financial Advisors ("NAIFA")':"NAIFA",
                     "National Association of Insurance and Financial Advisors":"NAIFA",
                     "National Conference of State Legislatures":"NACL",
                     'National Association of Realtors':'NAR',
                     'National Housing Conference':'NHC',
                     'National Securities Clearing':'NSC',
                     'National Stock Exchange':'NSE',
                     "Nationwide Insurance and Financial Services Inc":"Nationwide",      
                     'National Association of Independent Fee Appraisers':'NAIFA',
                     'National Association of Real Estate Investment Trusts':'NAREIT',
                     'National Association of Real Estate Investment':'NAREIT',
                     'National Association of Real Estate':'NAREIT',
                     "Nationwide Financial Services":"Nationwide",
                     "Nationwide":"Nationwide Financial Services",
                     "Nationwide Investment":"Nationwide",
                     "Nationwide Financial Service":"Nationwide",
                     'National Association for Fixed Annuities':'NAFA',
                     "National Bank Financial":"NBF",
                     "National Consumers League":"NCL",
                     "National Venture Capital Association":"NVCA",
                     "National Venture Capital Association.":"NVCA",
                     "National Venture Capital Associatio":"NVCA",
                     "National Futures Association":"NFS",
                     "National Mining Association":"NMA",
                     "National Retail Federatio":"NRF",
                     "National Association of Personal Financial Advisors":"NAPFA",
                     "National Asian American Coalitio":"NAAC",
                     "National Automobile Dealers Association":"NADA",
                     "New York Stock Exchange":"NYSE",
                     "NRGI and Oxfam":"NRGI",
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
                     "NYSE Euronext":"NYSE",
                     'North American Securities Administrators Association':'NASAA',
                     "Occupy":"Occupy the SEC",
                     "OTC Derivatives Regulators Forum members":"OTC Derivatives Regulators Forum",
                     "Options Clearing Corporation (OCC)":"OCC",
                     "Of Extractive Industries Transparency Initiative":"EITI",
                     "Office of US Senator Jeff Merkley":"Senator Jeff Merkley",
                     "Office of Senator Richard Durbin and from the office of Representative Jim McDermott":"Senator Richard Durbin",
                     "Offices of Senator Cardi":"Senator Cardin",
                     "Panel discussion with the Real Estate Investment Securities Associatio":"REISA",
                     "Panel discussion with the Real Estate Investment Securities Association":"REISA",
                     "Real Estate Investment Securities Associatio":"REISA",
                     "PNC Financial Services Group, Inc.":"PNC",
                     "Pan-Canadian Investors Committee for Third-Party Structured Asset-Backed Commercial Paper":"Pan Canadian Investors Committee",
                     "PNC Financial Services Group Inc":"PNC",
                     "PNC Financial Services Group":"PNC",
                     "Principal Financial Group":"Principal",
                     "Property Casualty Association of Americ":"Property Casualty Insurers Association of America",
                     "PWYP-US":"PWYP",
                     "Private Equity Growth Company Council":"Private Equity Growth Capital Council",
                     "Promontory Financial Group":"Promontory Financial",
                     "Prudential Financial":"Prudential",
                     "Publish What You Pay":"Publish What You Pay Coalitio",
                     "Putnam Investments Inc":"Putnam",
                     "Putnam  Investments":"Putnam",
                     "Paul A Volcker":"Paul Volcker",
                     "Pennsylvania Public School Employees?? Retirement System":"Pennsylvania Public School",
                     'Pennsylvania Public School Employees\x92 Retirement System':"Pennsylvania Public School",
                     "Personnel from SunGar":"SunGar",
                     "PCIPAC":"Property Casualty Insurers Association of America",
                     "Property Casualty Insurers Association of Americ":"Property Casualty Insurers Association of America",
                     "Public Investors Arbitration Bar Association":"PIABA",
                     "RBC Capital Markets":"RBC",
                     "RBC Wealth Management - U.S.":"RBC",
                     "RBC Capital Markets and Sullivan &\r\r\nCromwell":"RBC",
                     "RBS Securities Inc":"RBS",
                     "RBS Americas":"RBS",
                     "RBS Global Banking and Markets":"RBS",
                     "Real Estate Investment Securities Association":"REISA",
                     "Representatives organized  by the National Association of Manufacturers":"NAM",
                     "Representatives organized by the National Association of Manufacturers":"NAM",
                     "Royal Bank of Canada":"RBC",
                     "Robert Colby of Davis Polk Wardwell":"Davis Polk Wardwell",
                     'Risk Management Association ("RMA")':'RMA',
                     "Risk Management Association (RMA)":'RMA',
                     'Risk Management Association':"RMA",
                     "Rom the Division of Trading and Markets re: Meeting with the Capital Steering Committee of the Securities Industry and Financial Markets Association":"SIFMA",
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
                     "Securities Industry and Financial Markets Association":"SIFMA",
                     "Senators Merkley and Levins offices":"Senators Merkley",
                     'Securities Industry Association':'SIA',
                     'Security Traders Association':'STA',
                     "SIMFA":"SIFMA",
                     "Service Employees International Union":"SEIU",
                     "Social Investment Forum":"SIF",
                     'Society of Asset Allocators':'SAAFTI',
                     'Society of Asset Allocators and Fund Timers':'SAAFTI',
                     "Staff of Senator Jeff Merkley":"Senator Jeff Merkley",
                     'SocieteGenerale':'Society Generale',
                     "State Street Bank & Trust Company":"State Street",
                     "State Street Bank and Trust Company":"State Street",
                     "State Street":"State Street",
                     "SSgA":"State Street",
                     "State Street Corporation":"State Street",
                     "State Street Global Advisors":"State Street",
                     "Standard and Poor's Ratings Services":"Standard & Poor's Rating Services",
                     "State Farm VP Management Corp.":"State Farm",
                     "Stephens Inc.":"Stephens",
                     "Standard Poors Ratings Services":"Standard Poors Rating Services",
                     "S and P":"Standard Poors Rating Services",
                     "S&P":"Standard Poors Rating Services",
                     "Structured Credit International Corp":"SCIC",
                     "Sulllivan & Cromwell LLP":"Sullivan & Cromwell",
                     "Sullivan and Cromwell":"Sullivan & Cromwell",
                     "Sullivan & Cromwell Llp":"Sullivan & Cromwell",
                     "Sun Guar":"SunGar",
                     "Swaps and Derivatives Market Association (SDMA)":"SDMA",
                     "Swaps & Derivatives Market Association":"SDMA",
                     "Swaps & Derivatives Market Associatio":"SDMA",
                     "Swaps and Derivatives Market Associatio":"SDMA",
                     "Swaps and Derivatives Market Association":"SDMA",
                     "Securities Industry and Financial Markets Association (SIFMA) and Davis Polk Wardwell":"SIFMA",
                     "SVB Financial Group":"SVB",
                     "Silicon Valley Bank Financial Group":"SVB",
                     "Stable Value Industry Associatio":"Stable Value",
                     "Stable Value Firms":"Stable Value",
                     "Standard and Poors Ratings Services":"Standard Poors Ratings Services",
                     "Swaps Derivatives Market Associatio":"SDMA",
                     "Swaps Derivatives Market Association":"SDMA",
                     "Systemic Risk Council":"SRC",
                     "Swap Financial Group":"SFG",
                     "Representatives the Capital Steering Committee of the Securities Industry and Financial Markets Association (SIFMA)":"SIFMA",
                     'TWCMIG"':"TWCMIG",
                     "TD Ameritrade, Inc.":"TD Ameritrade",
                     "Trade repositories (TRs) and ISDA":"ISDA",
                     "Tradeweb":"TradeWeb",
                     "Trade Information Warehouse":"TIW",
                     "The Clearing House Association":"Clearing House",
                     "The Clearing House Association. Llc":"Clearing House",
                     "The Clearing House Association Llc":"Clearing House",
                     "The TCW Group":"TCW", 
                     "Tradeweb, LLC":"TradeWeb",
                     "Treasury Borrowing Advisory Committee":"TBAC",
                     "UBS Bank USA":"UBS",
                     "UK Regulated Covered Bond Council":"UKRCBC",
                     "US Chamber of Commerce Center for Capital Markets Competitiveness":"US Chamber of Commerce",
                     "US and International Banks":"IIB",
                     "US Chamber of Commerce Center":"US Chamber of Commerce",
                     "US SIF":"SIF",
                     "United Services Automobile Associatio":"USAA",
                     "Union Asset Management Holding AG":"Union Asset",
                     "University of Maryland Center for Health Homeland Security":"University of Maryland",
                     "Udy Group Meeting Notebook":"Udy Group",
                     "Chamber":"US Chamber of Commerce",
                     "Wells Fargo Advisors":"Wells Fargo",
                     "Wells Capital Management":"Wells Fargo",
                     "Wells Fargo Securities":"Wells Fargo",
                     "Western Asset Management Co.":"Western Asset Management",
                     "members of SIMFA":"SIFMA",
                     "the Financial Services Roundtable":"Financial Services Roundtable",
                     "Wholesale Markets Brokers?? Associatio":"WMBA",
                     'Wholesale Markets Brokers\x92 Association':"WMBA",
                     "Wholesale Markets Brokers?? Association":"WMBA",
                     'Wholesale Markets Brokers\x92 Associatio':"WMBA",
                     "Wholesale Market Brokers' Associatio":"WMBA",
                     "Wholesale Market Brokers Association":"WMBA",
                     "Dealer members of the Securities Industry and Financial Markets Associatio":"SIFMA",
                     "Rom the Division of Trading and Markets re: Meeting with the Capital Steering Committee of the Securities Industry and Financial Markets Associatio":"SIFMA",
                     "Rom the Division of Trading and Markets re: US Chamber of Commerce":"US Chamber of Commerce",
                     "Rom the Division of Trading and Markets regarding a series of August meetings with Peter Shapiro of Swap Financial Group":"Swap Financial Group",
                     "Yale Endowment":"Yale University",
                     "Yale School of Management":"Yale University",
                     }        
        if org in formal_name:
#            print("!!!")
            return tio_to_tion(strip_pron(is_org(formal_name[org])))
        else:
            return tio_to_tion(strip_pron(is_org(org)))
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
            part_score_t=fuzz.partial_ratio(stem_org(org),stem_org(Org))
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
    
def add_org(org,dic):
    if org in dic:
        dic[org]+=1
    else:
        dic[org]=1
        
        
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


def pdf_parse2(pdf_save_add):
    with open(pdf_save_add ,"rb") as pdfFileObj:
        pdfFileObj = open(pdf_save_add, 'rb')
    
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        N=pdfReader.numPages
        pageObj = pdfReader.getPage(0)
        S=pageObj.extractText()
#    pdfFileObj = open(pdf_save_add, 'rb')
#
#    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#    N=pdfReader.numPages
#    pageObj = pdfReader.getPage(0)
#    S=pageObj.extractText()
    
#    pdfFileObj.close()
    return S,N

def convery_pdf_to_txt(pdf_add):
    if ".pdf" in pdf_add:
        txt_save_add=pdf_add.replace(".pdf",".txt")
        if not os.path.exists(txt_save_add):
            with open(txt_save_add,"w") as f:
                f.write("0")
        pdf_or_not=1
        try:
            text,page_num=pdf_parse1(pdf_add)
            pdf_readable=1
        except:
            text,page_num=pdf_parse2(pdf_add)
            pdf_readable=0
        try:
            with open(txt_save_add,"w") as f:
                f.write(text.encode('latin-1', 'replace').decode("utf-8","ignore").replace("?"," "))   
        except:
            with open(txt_save_add,"w") as f:
                f.write("0")
        return pdf_or_not, pdf_readable, page_num
    else:
        return 0,0,0
            

def get_pdf_comments(pdf_url, file_name, file_basic_save_add,rule_i):
    pdf_save_add=file_basic_save_add+"\\"+file_name+".pdf"
    r=requests.get(pdf_url)
    try:
        if not os.path.exists(pdf_save_add):
            with open(pdf_save_add,"wb") as f:
                f.write(r.content)
        print("saving pdf for rule "+str(rule_i))
        print("saving comment "+file_name +" done")
    except:
        if not os.path.exists(pdf_save_add):
            with open(pdf_save_add,"wb") as f:
                f.write("0")
    return [pdf_save_add]
        
def get_htm_comments(htm_url, file_name, file_basic_save_add,rule_i):
    htm_save_add = file_basic_save_add+"\\"+file_name+".txt"
    soup=BeautifulSoup(requests.get(htm_url).text,"lxml")
    P=soup.find_all("p")
    A=soup.find_all("a")
    good_bye=soup.find_all("h1",class_="goodbye text-center")
    if not good_bye:
        if not A:
            text=""
            for p in P:
                text+=p.text
                text+="\n\n"
            text=text.encode('latin-1', 'replace').decode("utf-8","ignore").replace("?"," ")
            try:
                if not os.path.exists(htm_save_add):
                    with open(htm_save_add,"w",encoding="latin-1") as f:
                        f.write(text)
                print("saving pdf for rule "+str(rule_i))
                print("saving comment " +file_name + " done")
            except:
                if not os.path.exists(htm_save_add):
                    with open(htm_save_add,"w",encoding="latin-1") as f:
                        f.write("0")
            return [htm_save_add]
        else:
            return_list=[]
            for href_i in range(len(A)):
                
    #            return_list.append(file_name+"_"+str(href_i)+".pdf")
                htm_save_add = file_basic_save_add+"\\"+file_name+"_"+str(href_i)+".pdf"
                
                href=A[href_i]
                if ".pdf" in href:
                    return_list.append(htm_save_add)
                    comment_url="https://www.sec.gov"+href['href']
                    
                    r=requests.get(comment_url)
                    try:
                        if not os.path.exists(htm_save_add):
                            with open(htm_save_add,"wb") as f:
                                f.write(r.content)
                        print("saving pdf for rule "+str(rule_i))
                        print("saving comment " +file_name + " done")
                    except:
                        if not os.path.exists(htm_save_add):
                            with open(htm_save_add,"wb") as f:
                                f.write("0")
                else:
                    htm_save_add = file_basic_save_add+"\\"+file_name+"_"+str(href_i)+".txt"
                    return_list.append(htm_save_add)
                    if not os.path.exists(htm_save_add):
                        with open(htm_save_add,"w") as f:
                            f.write("0")
                
                
            return return_list
    else:
        if not os.path.exists(htm_save_add):
            with open(htm_save_add,"w",encoding="latin-1") as f:
                f.write("0")
        return [htm_save_add]


def download_comment(comment_url, file_name, file_basic_save_add,rule_i):
    if comment_url.endswith(".pdf"):
        comment_filename_list=get_pdf_comments(comment_url,file_name, file_basic_save_add,rule_i)
    else:
        comment_filename_list=get_htm_comments(comment_url,file_name, file_basic_save_add,rule_i)
    return comment_filename_list
        

        

rule_type_dic={}
rule_type_list=SEC_comments_data["rule type"].unique()
for i in range(len(rule_type_list)):
    rule=rule_type_list[i]
    rule_type_dic[rule]=i


threshold=51
count=0
count_c=0
amb_match_dic=[]
SEC_comment_org=[]
no_match=[]
match=[]

rule_type_list=SEC_comments_data["rule type"].unique()

newpath_basic=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\download\SEC_comments"
for i in range(len(rule_type_list)):
    newpath = newpath_basic+"\\rule_"+str(i)
    if not os.path.exists(newpath):
        os.makedirs(newpath)

comment_scrape_result_save_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\scrape_comment_result_SEC"
#rule_type_list=list(rule_type_list[10])
org_match_dic={}
for org in org_for_see:
    org_match_dic[org]=0
final_rule_good=[0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]
#for i in range(500,1000):
#for i in range(37,len(rule_type_list)):
#for i in range(10,11):
for i in range(20,len(rule_type_list)):
#for i in range(0,1):
    if i not in final_rule_good:
    
        print("rule: "+str(i))
        comment_scrape_result=[]
        comment_save_basic_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw\download\SEC_comments\rule_"+str(i)
        
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
            comment_url=row["url"]
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
                        add_org(org_candidate,org_match_dic)
                           
                        comment_file_name_1 = org_candidate + "_" + str(small_group_result[org_candidate])
                        comment_file_name_list = download_comment(comment_url, comment_file_name_1, comment_save_basic_add,i)
                        for comment_file_name in comment_file_name_list:
#                                if comment_file_name ==0:
                        
                            comment_scrape_result.append({})
                            comment_scrape_result[-1]["comment"]=org_inf
                            comment_scrape_result[-1]["rule type"]=i
                            comment_scrape_result[-1]["url"]=comment_url
                            comment_scrape_result[-1]["identify org"]=org_candidate
                            comment_scrape_result[-1]["file name"]=comment_file_name
                            try:
                                pdf_ind, readable_ind, pdf_page_N=convery_pdf_to_txt(comment_file_name)
                            except:
                                pdf_ind, readable_ind, pdf_page_N=1,0,0
                            
                            comment_scrape_result[-1]["pdf or not"] = pdf_ind
                            comment_scrape_result[-1]["pdf readable"] = readable_ind
                            comment_scrape_result[-1]["pdf page number"] = pdf_page_N
                            
    
                    else:
        #                org_candidate=org_candidate.lower() 
                        success_i,org_m = match_org(org_candidate, org_clean,threshold)
        #                count+=success_i
                        if success_i:
        #                    amb_match_dic.append({org_candidate:org_m})
                            match_i=1
                            add_org(org_m,small_group_result)
                            add_org(org_m,org_match_dic)
                            
                            comment_file_name_1 = org_m + "_" + str(small_group_result[org_m])
                            comment_file_name_list = download_comment(comment_url, comment_file_name_1, comment_save_basic_add,i)
                            for comment_file_name in comment_file_name_list:
                            
                                comment_scrape_result.append({})
                                comment_scrape_result[-1]["comment"]=org_inf
                                comment_scrape_result[-1]["rule type"]=i
                                comment_scrape_result[-1]["url"]=comment_url
                                comment_scrape_result[-1]["identify org"]=org_m
                                comment_scrape_result[-1]["file name"]=comment_file_name   
                                try:
                                    pdf_ind, readable_ind, pdf_page_N=convery_pdf_to_txt(comment_file_name)
                                except:
                                    pdf_ind, readable_ind, pdf_page_N=1,0,0
                                
                                
                                comment_scrape_result[-1]["pdf or not"] = pdf_ind
                                comment_scrape_result[-1]["pdf readable"] = readable_ind
                                comment_scrape_result[-1]["pdf page number"] = pdf_page_N
                            
                            
                            
                            
            if not match_i:
                add_org("Individual",small_group_result)
                comment_file_name_1 = "Individual" + "_" + str(small_group_result[org_m])
                comment_file_name_list = download_comment(comment_url, comment_file_name_1, comment_save_basic_add,i)
                for comment_file_name in comment_file_name_list:
                
                    comment_scrape_result.append({})
                    comment_scrape_result[-1]["comment"]=org_inf
                    comment_scrape_result[-1]["rule type"]=i
                    comment_scrape_result[-1]["url"]=comment_url
                    comment_scrape_result[-1]["identify org"]="Individual"
                    comment_scrape_result[-1]["file name"]=comment_file_name 
                    try:
                        pdf_ind, readable_ind, pdf_page_N=convery_pdf_to_txt(comment_file_name)
                    except:
                        pdf_ind, readable_ind, pdf_page_N=1,0,0
                    comment_scrape_result[-1]["pdf or not"] = pdf_ind
                    comment_scrape_result[-1]["pdf readable"] = readable_ind
                    comment_scrape_result[-1]["pdf page number"] = pdf_page_N
                    
        scrape_result_save_pickle_add = comment_scrape_result_save_add + "\\" + str(i) + ".pickle"
        pickle.dump(pd.DataFrame(comment_scrape_result), open(scrape_result_save_pickle_add,"wb"))   


#save_pickle_add_m=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_comments_match_condition"+".pickle"
#pickle.dump(org_match_dic, open(save_pickle_add_m,"wb"))   
        
#t=pd.DataFrame(comment_scrape_result) 
#t.to_csv(r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"+"\\1.csv")       
#
#
#with open(scrape_result_save_pickle_add,"rb") as f:
#    tem=pickle.load(f, encoding='latin1')
#t=pd.DataFrame(tem)




























