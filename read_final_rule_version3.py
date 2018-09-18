# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 16:10:25 2018

@author: DongliangLu
"""

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
             "And Labaton Sucharow"
            ]
    if org in not_org or org.startswith("certain"):
        return "Individual"
    else:
        return org

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
    
punctuation=list(string.punctuation)
punctuation.remove("&")
punctuation.remove("/")
punctuation.remove("(")
punctuation.remove(")")
punctuation.append("´ ")
punctuation.append("’")

def strip_pron(org):
    pron=[",","'",".","´ "]
    if "&" in org:
        org = " ".join([i.strip() for i in org.split("&")])
    if "/" in org:
        org = " ".join([i.strip() for i in org.split("/")])
    for p in pron:
        if p in org:
            org=org.replace(p,"")
    return org

def tio_to_tion(org):
    org_l=org.split()
    if "Associatio" in org_l:
        org_l[org_l.index("Associatio")]="Association"
    if "Corporatio" in org_l:
        org_l[org_l.index("Corporatio")]="Corporation"
    return " ".join(org_l)

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

        formal_name={"American Bakers' Association": "ABA",
                     "American bakers' association":"ABA",
                     "American Bankers Association":"ABA",
                     "American Bankers' Association":"ABA",
                     "American for Financial Reform":"Americans for Financial Reform",
                     "AFR":"Americans for Financial Reform",
                     "ABASA":"ABA",
                     "Caleb Gibson of Americans for Financial Reform":"Americans for Financial Reform",
                     "Ameriprise Financial":"Ameriprise",
                     "American Council of Life Insurers":"ACLI",
                     "Alternative Investment Management Association (AIMA)":"AIMA",
                     "Alternative Investment Management Associatio":"Alternative Investment Management Association",
                     "Alternative Investment Management Association":"AIMA",
                     "Air Transportation Association":"ATA",
                     "Advanced Practice Advisors":"APA",
                     "American Benefits Council":"ABC",
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
                     "California Public Employees' Retirement System":"CalPERS",
                     "California Public Employees Retirement System":"CalPERS",
                     "California State Teachers Retirement System":"CalPERS",
                     "Canadian Banks and the Canadian Bankers?? Associatio":"Canadian Banks and the Canadian Bankers Association",
                     "Canadian Banks and the Canadian Bankers Associatio":"Canadian Banks and the Canadian Bankers Association",
                     "Canadian Securities Administrators":"CSA",
                     'Center for Capital Markets Competitiveness event on "Over the Counter (OTC) Derivatives Reform: Preparing for a Changing Marketplace"':'Center for Capital Markets Competitiveness',
                     "Certified Financial Planner Board of Standards":"CFP",
                     "CFA Inst":"CFA",
                     "CFTC and certain pension plans":"CFTC",
                     "CRE Finance Council":"CRE",
                     "Center for Study of Financial Market Evolution (CSFME)":"CSFME",
                     "Conference call CRE Finance Council":"CRE",
                     "Citi":"Citigroup",
                     "Citigroup Inc":"Citigroup",
                     "Citibank":"Citigroup",
                     "citibank":"Citigroup",
                     "Clearly":"Cleary Gottlieb",
                     "Cleary":"Cleary Gottlieb",
                     "Cleary Gottlieb Steen Hamilton":"Cleary Gottlieb",
                     "Chicago Mercantile Exchange Group":"CME",
                     "Cleary Gottlieb Steen Hamilto":"Cleary Gottlieb",
                     "Cleary Gottlieb & Steen Hamilto":"Cleary Gottlieb",
                     "Cleary Gottlieb and Steen Hamilto":"Cleary Gottlieb",
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
                     "Fixed Income Forum and Credit Roundtable":"Credit Roundtable and Fixed Income Forum",
                     "Davis Polk":"Davis Polk Wardwell",
                     "Davis Polk and Wardwell":"Davis Polk Wardwell",
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
                     "Dealer members of the Securities Industry and Financial Markets Association":"SIFMA",
                     "Depository Trust and Clearing Corporatio":"Depository Trust and Clearing Corporation",
                     "Depository Trust Clearing Corporation":"Depository Trust and Clearing Corporation",
                     "Discovery":"Discovery Capital Management",
                     "Discover Financial Services":"Discovery Capital Management",
                     "EquiLe":"Equile",
                     "Ed Rosen of Cleary Gottlieb Steen Hamilton":"Cleary Gottlieb",
                     "ExxonMobil":"Exxon Mobil",
                     "Exxon Mobil Corporation":"Exxon Mobil",
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
                     "Fixed Income Forum Credit Roundtable":"Credit Roundtable and Fixed Income Forum",
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
                     "Jefferies & Company":"Jefferies",
                     "Jewelers of Americ":"JA",
                     "LLP; and Kenney & McCafferty":"Kenney & McCafferty",
                     "Laborers?? International Union of North Americ":"International Union of North America",
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
                     "Nationwide Insurance and Financial Services Inc":"Nationwide",              
                     "Nationwide Financial Services":"Nationwide",
                     "Nationwide":"Nationwide Financial Services",
                     "Nationwide Investment":"Nationwide",
                     "Nationwide Financial Service":"Nationwide",
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
                     "Pan-Canadian Investors Committee for Third-Party Structured Asset-Backed Commercial Paper":"Pan-Canadian Investors Committee",
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
                     "SIMFA":"SIFMA",
                     "Service Employees International Union":"SEIU",
                     "Social Investment Forum":"SIF",
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
                     "Wholesale Markets Brokers?? Association":"WMBA",
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

def is_citation_has_org(citation):
    see_pattern=re.compile("\d+\s+See")
#    if re.match(see_pattern,citation):
    if re.search(see_pattern,citation):
        return 1
    else:
        return 0
    
def is_citation(citation):
    see_pattern=re.compile("\d+\s+[A-Za-z]")
#    if re.match(see_pattern,citation):
    federal_pattern=re.compile("\d+\s+Federal")
    if re.match(federal_pattern,citation):
#        print(citation)
        return 0
    if re.search(see_pattern,citation):
        return 1
    else:
        return 0

def find_bracket(citation):
    contain_bra=0
    for i in range(len(citation)):
        if citation[i]=="(":
            if contain_bra==0:
                s=i
            contain_bra+=1
        if citation[i]==")":
            if contain_bra!=0:
                if contain_bra==1:
                    e=i
                    return s,e
                else:
                    contain_bra-=1
            else:
                pass
    return s,len(citation)
        
def remove_at(org):
    at_pattern=re.compile("\sat\s")
    if re.search(at_pattern,org):
        s=re.search(at_pattern,org).start()
        return org[:s]
    return org
            

#month=["Jan","Feb","Mar","Apr","May",""]
def remove_bracket_inf(citation):
    while "(" in citation:
        s,e=find_bracket(citation)
        citation=citation[:s]+citation[e+1:]
    if ")" in citation:
        citation=citation[citation.find(")")+1:]
    return citation

bracket_pattern=re.compile("((.+?))")


def remove_extra(citation):
    extra=[", e.g., ","et al."]
    for e in extra:
        citation=citation.replace(e,"")
    return citation

replace_dic={'Ass’n.':"Assocation",
             "Ass'n.":"Assocation",
             "Ass'n":"Assocation",
             'Ass’n':"Assocation",
             "BoA":"Bank of America Merrill Lynch",
             "BoA.":"Bank of America Merrill Lynch",
             "Sens.":"Senator",
             "Prof.":"Professor",
             "Mgmt.":"Management",
             "Am.":"American",
             "Govt.":"Government",
        }
def replace_abb(citation):
    citation_l=citation.split()#here it also split \n, because if you print it here, it is " "
    for i in range(len(citation_l)):
        if citation_l[i] in replace_dic:
            citation_l[i]=replace_dic[citation_l[i]]
    return " ".join(citation_l)
    
def strip_letter_from(org):
    Letter=["letter","Letter","letters","Letters","From","from","See"]
    org=org.strip()
    org=org.lstrip("and").strip()
    for l in Letter:
        org=org.replace(l,"")
    return " ".join(org.split())

def append_org_word(orgs_l,stop):
    org_return=orgs_l[0]
    orgs_l=orgs_l[1:]
    while orgs_l and porter_stemmer.stem(orgs_l[0].lower()) in stop:
        org_return+=" "
        org_return+=orgs_l[0]
        orgs_l=orgs_l[1:]
    return org_return
        
    
    


def find_citation_num(citation_m):
    if type(citation_m)!=list:
        citation_m=[citation_m]
    numbers_in_citation_s=[]
    num_pattern=re.compile("\d+")
    num_pattern2=re.compile("\\n\d+\sSee")
    for i in range(1, min(len(citation_m),80) ):
#        if "70897" in citation_m[-i]:
#            print(citation_m[-i])
        
        if re.match(num_pattern,citation_m[-i]):
            number_match=re.match(num_pattern,citation_m[-i]).group()
            numbers_in_citation_s.append(int(number_match))
        if re.findall(num_pattern2,citation_m[-i]):
            tem=re.findall(num_pattern2,citation_m[-i])[-1]
            number_match=re.search(num_pattern,tem).group()
            numbers_in_citation_s.append(int(number_match))
    numbers_in_citation_s.sort()
    size=len(numbers_in_citation_s)
    median_index=size//2
    median=numbers_in_citation_s[median_index]
    
    numbers_in_citation_s=[i for i in numbers_in_citation_s if i>= median-size*2 and i<= median+size*2  ]
#    print(numbers_in_citation_s)
#    print(max(numbers_in_citation_s))
    return max(numbers_in_citation_s)




save_pickle_add2=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_meeting_small_rule.pickle"
#pickle.dump(SEC_meeting_all, open(save_pickle_add2,"wb"))
with open(save_pickle_add2,"rb") as f:
    tem=pickle.load(f, encoding='latin1')
dataframe_meeting=tem
org_set=dataframe_meeting["organization"].unique()
org_set=set(org_set)
new_org=["Prudential","Renaissance","Putnam","American Express",
         "Japanese Bankers Assocation","Invesco","CalPERS","Vanguard",
         "CIEBA","FTN","FSA","NACL","NAMIC","UKRCBC","TCW","BBVA","Western Asset Management","Union Asset"]
new_org=set(new_org)
org_set=org_set|new_org
org_for_see=list(org_set)
org_for_see.sort()


#stem_word_in_org=set()
#stop_add=[]
#for words in org_set:
#    word_l=words.split()
#    for word in word_l:
#        candi=porter_stemmer.stem(word).lower()
#        if candi not in stop:
#            if candi in stem_word_in_org:
#                stop_add.append(candi)
#            else:
#                stem_word_in_org=stem_word_in_org|set([candi])
#
#too_frequent=["a","admiinistr","afric","africa","bar","best","buy",
#              "better","broker","commissio","commission","common",
#              "congress","econom","entiti","exchang","first","global",
#              "implement","leader","london","micro","new","p","pay","resourc",
#              "research","york","one","franc","french","polici","structur",
#              "notebook","underwrit","delta","foreign","loan","personal",
#              "natur","relat","growth","borrow","meet","organ","benefit",
#              'practic','strategi']
#too_fre_set=set(too_frequent)
#stop=stop1+stop2+stop_add
#stop=set(stop)
#org_dic={}
#org_words_set=[]
#for words in org_set:
#    word_l=words.split()
##    ind=0
#    for word in word_l:
#        candi=porter_stemmer.stem(word).lower()
#        org_words_set.append(candi)
#        if candi not in stop and candi not in too_fre_set:
#            org_dic[candi]=words
##            ind=1
#        
#org_words_set=set(org_words_set)
#o=list(org_words_set)
#o.sort()




final_rule_good=[0,2,5,6,7,8,9,10,12,16,30,31,32,33,35,36]
#final_rule_good=[10]
final_rule_good=[2]
citation_percent=[]
for i_large in range(0,len(final_rule_good)):
    read_rule_num=final_rule_good[i_large]
    print(read_rule_num)
    path_basic=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\final rule\SEC_rule\final"
    path=path_basic+"\\"+str(read_rule_num)+".pdf"

    raw_S,npag=pdf_parse1(path)
    #raw_S[32900:33800]
    
    _pat=re.compile("\\n\\n[A-Za-z]")
    _pat=re.compile("\\n\\n\d+")
    
    #citation_pattern=re.compile("\\n\\n\d+.*\\n\\n[A-Za-z]",re.S)#will return only one very long
    #citation_pattern=re.compile("\\n\\n\d+.*(\\n\\n[A-Za-z]+?)",re.S)
    #citation_pattern=re.compile("\\n\\n\d+.*((\\n\\n[A-Za-z])+?)",re.S)
    citation_pattern=re.compile("\\n\\n(\d+.*?)\\n\\n[A-Za-z]",re.S)
    #tem = re.findall(citation_pattern,raw_S[32900:33800])
    #print(tem)
    citation_all = re.findall(citation_pattern,raw_S)
    Citation_merge=[]
    Citation_total=[]
    for c in citation_all:
        if is_citation_has_org(c):
            Citation_merge.append(c)
        if is_citation(c):#not contain federal...
            Citation_total.append(c)
    if Citation_total:
        citation_num=find_citation_num(Citation_total)
    else:
        citation_num=0
    
    Citation=[]
    start_pattern=re.compile("\n\d+\s+See")
    start_strip_pattern=re.compile("\d+\s+See")
    for c in Citation_merge:
#        start_strip=re.match(start_strip_pattern,c).span()[1]
        start_strip=re.search(start_strip_pattern,c).span()[1]
        c=c[start_strip:]
        cspan = re.search(start_pattern,c)
        while cspan:
            citation=c[: cspan.span()[0]]
            Citation.append(citation.strip())
            c=c[cspan.span()[1]:]
            cspan = re.search(start_pattern,c)
        Citation.append(c.strip())
        
    
    Number=[]
    for number in range(10):
        Number.append(str(number))
    not_org=["rule","§","Proposal","http:","Form"]
    #ignore citations not contain any org
    #those citations usually contains "rule", "number but not date", but not always right...
    Citation_has_org=[]
    count=0
    for i in range(0,len(Citation)):
    #for i in range(0,200):
        C=Citation[i]
        not_ind=0
        for n in not_org:
            if n in C:
                not_ind=1
        for n in Number:
            if C[0]==n:
                not_ind=1
        if not_ind==0:
            if ";" in C:
                Citation_has_org.append(C)
            else:
                if "\n" not in C:
                    count_number=0
                    for w in C:
                        if w in Number:
                            count_number+=1
                    if count_number<=0.2*len(C):
                        Citation_has_org.append(C)
                    else:
                        pass
                else:
                    Citation_has_org.append(C)
                            
    
    
    
    #should deal with and, rule 12
    #deal with more than one see in the one citation
    
    
    
    Org_citation=[]
    not_an_org_l=[]
    citation_contains_org=0
    for i in range(len(Citation_has_org)):
    #for i in range(100):
#        print(i)
        citation_contains_add_indicator=0
        orgs_c=Citation_has_org[i]
        orgs_c=remove_bracket_inf(orgs_c)
        orgs_c=remove_extra(orgs_c)
        orgs_c=" ".join(orgs_c.split())
        if ";" in orgs_c:
            orgs_c_l=orgs_c.split(";")
        else:
            orgs_c_l=orgs_c.split(",")
        
        see_also_pattern=re.compile("[Ss]ee also")
        orgs_c_l2=[]
        for orgs in orgs_c_l:
            if re.search(see_also_pattern, orgs):
                orgs_c_l2.append(orgs[:re.search(see_also_pattern, orgs).start()].strip())
                orgs_c_l2.append(orgs[re.search(see_also_pattern, orgs).end():].strip())
            else:
                orgs_c_l2.append(orgs)
                
        for orgs in orgs_c_l:
            if " and " in orgs:
                orgs_c_l2.extend(orgs.split(" and "))
            if "/" in orgs:
                orgs_c_l2.extend(orgs.split("/"))
                
        for orgs in orgs_c_l2:
            
            orgs=strip_letter_from(orgs)
            orgs=remove_at(orgs)
            
            if len(orgs.split())>=8:#"See also"
                orgs=append_org_word(orgs.split(),stop)
            orgs=replace_abb(orgs.strip()).strip(".").strip()   
            orgs=rewrite_orgname(orgs)
            if orgs in org_set:
                citation_contains_add_indicator=1
                Org_citation.append(orgs)
            elif abbize(orgs,stop1) in org_set:
                citation_contains_add_indicator=1
                Org_citation.append(abbize(orgs,stop1))
            else:
                if orgs.split():
                    find_ind=0
                    for l in range( min(7,len(orgs.split()) ) ):
                        orgs_f=" ".join(orgs.split()[:l+1])#has some problem here,will under estimate
                        orgs_f=replace_abb(orgs_f.strip()).strip(".").strip()
                        orgs_f=rewrite_orgname(orgs_f)
                        orgs_abb=abbize(orgs_f,stop1)
                        if orgs_f in org_set:
                            citation_contains_add_indicator=1
                            Org_citation.append(orgs_f)
                            find_ind=1
                        elif orgs_abb in org_set:
                            citation_contains_add_indicator=1
                            Org_citation.append(orgs_abb)
                            find_ind=1
                    if find_ind==0:
                        not_an_org_l.append(orgs)
        citation_contains_org+=citation_contains_add_indicator
            
    org_for_see2=Org_citation
    not_an_org_l_2=list(set(not_an_org_l))
    not_an_org_l_2.sort()
    
    
    org_citation={}
    for org in org_set:
        org_citation[org]=0
    for org_c in Org_citation:
        org_citation[org_c]+=1
    
    citation_result_list=[]
    for org in org_citation.keys():
        citation_result_list.append({})
        citation_result_list[-1]["organization"]=org
        citation_result_list[-1]["citation"]=org_citation[org]
    #    citation_result_list[-1]["rule type"]=rule_type
        citation_result_list[-1]["rule type number"]=read_rule_num
        
    save_pickle_add_i=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_citation"+str(read_rule_num)+".pickle"
    pickle.dump(citation_result_list, open(save_pickle_add_i,"wb")) 
    citation_percent.append({})
    citation_percent[-1]["rule type number"]=read_rule_num
    citation_percent[-1]["total citation"]=citation_num
    citation_percent[-1]["citation contains org"]=citation_contains_org
    citation_percent[-1]["citation citing rules"]=len(Citation)-citation_contains_org
    citation_percent[-1]["citation stating details"]=citation_num-len(Citation)
    
#save_pickle_citation_percentage=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_citation_percentage"+".pickle"
#pickle.dump(citation_percent, open(save_pickle_citation_percentage,"wb")) 








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
#final_rule_good=[10]
#
#for i_large in range(0,len(final_rule_good)):
#    read_rule_num=final_rule_good[i_large]
#    print(read_rule_num)
#    path_basic=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\final rule\SEC_rule\final"
#    path=path_basic+"\\"+str(read_rule_num)+".pdf"
#    S,npag=pdf_parse1(path)
#    #path_save=path_basic+"\\final_rule_banking_1.txt"
#    #with open(path_save, 'w') as f:
#    #    f.write(str(S))
#    #len(S.split())
#    
#    S=S.replace("\n"," ").replace("'"," ").replace("\\"," ")
#    #S=" ".join([strip_pron(i) for i in S.split() if i not in punctuation])#since we replace "&" by " ", it's better to return a string not a list
#    S=" ".join([strip_pron(i) for i in S.split()])
#    word_in_S=S.split()
#    Voc=""
#    continuous_ind=""
#    for word in word_in_S:
#        if porter_stemmer.stem(word).lower() in org_words_set:
#            Voc+=continuous_ind
#            Voc+=word
#            Voc+=" "
#            continuous_ind=""
#        else:
#            continuous_ind="1 "
#    
#    if Voc[0]=="1":
#        Voc=Voc[2:]
#    word_in_S_n=Voc.split(" 1 ")
#    
#    
#    org_citation={}
#    for org in org_set:
#        org_citation[org]=0
#    
#    not_match_word=[]
#    for word in word_in_S_n:
#        spl_word=word.split()
#        find_org_ind=0
#        tem_org=""
#        for s_word in spl_word:
#            stem_word=porter_stemmer.stem(s_word).lower()
#            if stem_word in org_dic:
#                org_find=org_dic[stem_word]
#                if org_find != tem_org:
#                    org_citation[org_find]+=1
#                    find_org_ind=1
#                    tem_org=org_find
#        if find_org_ind==0:
#            possi_Cov=[]
#            for voc_i in range(1,min(7, len(spl_word))):
#    #            Voc.append([])
#    #            tem=""
#                for i in range(len(spl_word)-voc_i):
#                    tem=" ".join(word_in_S[i:i+voc_i])
#    #                Voc[-1].append(rewrite_orgname(tem))
#                    rt=rewrite_orgname(tem)
#                    at=abbize(tem,stop1)
#                    if rt in org_set:
#                        org_citation[rt]+=1
#                    elif at in org_set:
#                        org_citation[at]+=1
#                    else:
#                        pass
#                        
#                
#    
#    #volcker rule: 1, 10
#    citation_result_list=[]
#    for org in org_citation.keys():
#        citation_result_list.append({})
#        citation_result_list[-1]["organization"]=org
#        citation_result_list[-1]["citation"]=org_citation[org]
#    #    citation_result_list[-1]["rule type"]=rule_type
#        citation_result_list[-1]["rule type number"]=read_rule_num
#        
#    save_pickle_add_i=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_citation"+str(read_rule_num)+".pickle"
#    pickle.dump(citation_result_list, open(save_pickle_add_i,"wb"))   
#    
#
#with open(save_pickle_add_i,"rb") as f:
#    tem=pickle.load(f, encoding='latin1')




    
    
    
    
    
    
    
    
    
    
    



        
        
        