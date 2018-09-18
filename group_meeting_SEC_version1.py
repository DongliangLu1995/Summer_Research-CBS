# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 10:06:03 2018

@author: DongliangLu
"""

#group_meeting_SEC
import pandas as pd
import re
import pickle
#first deal with ",", then deal with "and"

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
    pron=[",","'","."]
    if "&" in org:
        org = " ".join([i.strip() for i in org.split("&")])
    for p in pron:
        if p in org:
            org=org.replace(p,"")
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
                     "Goldman":"Goldman Sachs",
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
                     "RBC Capital Markets and Sullivan &\r\r\nCromwell":"RBC",
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

def add_org(dic, inf):
    if inf:
        if type(inf)==list:
            for i in inf:
                if i:
                    if rewrite_orgname(capitalize_first(i)) in dic:
                        dic[rewrite_orgname(capitalize_first(i))]+=1
                    else:
                        dic[rewrite_orgname(capitalize_first(i))]=1 
        else:
            if rewrite_orgname(capitalize_first(inf)) in dic:
                dic[rewrite_orgname(capitalize_first(inf))]+=1
            else:
                dic[rewrite_orgname(capitalize_first(inf))]=1
#don't need to return here, the dic will automically change


def deal_bad_raw_org(org):
    #for these org almost done
    if "with" in org:
        w_pattern=re.compile("with")
        start=re.search(w_pattern,org).span()[1]
        org_new=strip_comma(org[start:])
#        add_org(dic,rewrite_orgname(org_new))
        orgs_new=sepe_and(org_new)
        if type(orgs_new)==list:
            return [rewrite_orgname(i) for i in orgs_new]
        else:
            return orgs_new

                
#        z.append(org_new)
    elif "between" in org:
        b_pattern=re.compile("between")
        start=re.search(b_pattern,org).span()[1]
        org_new=strip_comma(org[start:])
#        add_org(dic,rewrite_orgname(org_new))
        orgs_new=sepe_and(org_new)
        if type(orgs_new)==list:
            return [rewrite_orgname(i) for i in orgs_new]
        else:
            return orgs_new

    else:
#        print(org)
        pass#pure number
    
def deal_normal_raw_org(org):
    org.strip("of ")
    bad_list=["members of",
              "representative from",
              "representative of",
              "staff from",
              "teleconference with",
              "telephone conference with",
              "Representatives from",
              "Representatives of",
              "Representative of",
              "telephone conversation with"
              ]
    for bad in bad_list:
        if bad in org:
            bad_pattern=re.compile(bad)
            start=re.search(bad_pattern,org).span()[1]
            org_new=strip_comma(org[start:])
            org_new=rewrite_orgname(org_new)
            orgs_new=sepe_and(org_new)
            if type(orgs_new)==list:
                return [rewrite_orgname(i) for i in orgs_new]
            else:
                return orgs_new
        else:
            pass
    orgs_new=sepe_and(org)
    if type(orgs_new)==list:
        return [rewrite_orgname(i) for i in orgs_new]
    else:
        return orgs_new




def seperate_org(orgs):
#    not_an_org=("Firm","Public Citize","Public Citizen","Usaa","Inc.","L.P.",""," ","LLP","et al.","LLC")
    not_an_org=("Firm","Public Citize","Public Citizen","Usaa",""," ","et al.")    
    orgs=strip_comma(orgs)
    orgs=orgs.split(",")
    orgs = [strip_comma(org).strip("and ") for org in orgs if (strip_comma(org) not in not_an_org)]
    if len(orgs)!=1:
        orgs_new=[]
        for i in range(len(orgs)):
#            if orgs[i]=="L.P.":
#                orgs_new[-1]=orgs_new[-1]+", LLP"
#            elif orgs[i]=="LLP":
#                orgs_new[-1]=orgs_new[-1]+", LLP"    
#            elif orgs[i]=="LLP.":
#                orgs_new[-1]=orgs_new[-1]+", LLP"
#            elif orgs[i]=="Inc.":
#                orgs_new[-1]=orgs_new[-1]+", Inc."
#            elif orgs[i]=="Inc":
#                orgs_new[-1]=orgs_new[-1]+", Inc."    
#            elif orgs[i]=="LLC":
#                orgs_new[-1]=orgs_new[-1]+", LLC"
            if orgs[i] in ["LLP","L.P.","Inc.","LLC","LLP."]:
                pass
            else:
                
                orgs_new.append(orgs[i])
        return orgs_new
    
    return orgs
    
    
    
data_add=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\raw"
SEC_meeting_data=pd.read_csv(data_add+"\\SEC_meetings.csv",index_col=0)
#SEC_meeting_data.drop(SEC_meeting_data.columns[0],axis=1, inplace=True)    

#calculate organization for total rules
SEC_org={}
#orgs_new=[]
#z=[]
for i in range(len(SEC_meeting_data)):
    
    orgs = SEC_meeting_data.loc[i,"organization"]
    for org in seperate_org(orgs):#deal with ","
        org=rewrite_orgname(org)
        
        d_pattern=re.compile(".*\d+")
        if re.search(d_pattern, org ):# has a number
            org=deal_bad_raw_org(org)#also deal with "and"
            add_org(SEC_org,org)
        else:
            org=deal_normal_raw_org(org)#also deal with "and"
            add_org(SEC_org,org)




save_pickle_add1=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_meeting_total.pickle"
pickle.dump(SEC_org, open(save_pickle_add1,"wb"))
with open(save_pickle_add1,"rb") as f:
    tem=pickle.load(f, encoding='latin1')


#first group the dataframe by rule_type, and then calculate seperately

SEC_org_per_rule=[]

#rule_type_list=SEC_meeting_data["rule type"].value_counts()
rule_type_list=SEC_meeting_data["rule type"].unique()
SEC_meeting_all=pd.DataFrame()
for rule in rule_type_list:
    small_dataframe=SEC_meeting_data[SEC_meeting_data["rule type"]==rule]
    small_group_result={}
    for index, row in small_dataframe.iterrows():
#        orgs = small_dataframe.loc[i,"organization"]
        orgs = row["organization"]
        for org in seperate_org(orgs):#deal with ","
            org=rewrite_orgname(org)
            
            d_pattern=re.compile(".*\d+")
            if re.search(d_pattern, org ):# has a number
                org=deal_bad_raw_org(org)#also deal with "and"
                add_org(small_group_result,org)
            else:
                org=deal_normal_raw_org(org)#also deal with "and"
                add_org(small_group_result,org)
    small_group_result_list=[]
    for key in small_group_result.keys():
        small_group_result_list.append({})
        small_group_result_list[-1]["organization"]=key
        small_group_result_list[-1]["meeting times"]=small_group_result[key]
        small_group_result_list[-1]["rule type"]=rule
        
    dataframe_small=pd.DataFrame(small_group_result_list)
    SEC_meeting_all=SEC_meeting_all.append(dataframe_small,ignore_index=True)
        
save_pickle_add2=r"C:\Users\DongliangLu\Desktop\Columbia\research\CBS\lobby\data_cleaned"+"\\SEC_meeting_small_rule.pickle"
pickle.dump(SEC_meeting_all, open(save_pickle_add2,"wb"))
with open(save_pickle_add2,"rb") as f:
    tem=pickle.load(f, encoding='latin1')


rule_type_grouped=SEC_meeting_all["meeting times"].groupby(SEC_meeting_all["rule type"])
sum_rule_type=rule_type_grouped.sum()
sum_rule_type=sum_rule_type.sort_values(ascending=False)
show1=sum_rule_type[:10]

org_type_grouped=SEC_meeting_all["meeting times"].groupby(SEC_meeting_all["organization"])
sum_org_type=org_type_grouped.sum()
sum_org_type=sum_org_type.sort_values(ascending=False)
show2=sum_org_type[:11]


   
    

































