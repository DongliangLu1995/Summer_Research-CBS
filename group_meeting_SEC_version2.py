# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 09:28:22 2018

@author: DongliangLu
"""

#group_meeting_SEC version2
import pandas as pd
import re
import pickle
#first deal with ",", then deal with "and"

#steps to rewrite an org name:
#1. strip" ", seperate and strip" "
#2. drop "the","inc",...
#3. rewrite to the unified formal name, should avoid high frequency words
#4. strip "&", "."...
#5. to see whether it's an org

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
    pron=[",","'","."]
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
                     'Canadian Banks and the Canadian Bankers\x92 Association':"Canadian Banks and the Canadian Bankers Association",
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

def add_org(dic, inf):
    if inf:
        if type(inf)==list:
            for i in inf:
                if i:
                    I=rewrite_orgname(capitalize_first(i))
                    if I in dic:
                        dic[I]+=1
                    else:
                        dic[I]=1 
        else:
            I=rewrite_orgname(capitalize_first(inf))
            if I in dic:
                dic[I]+=1
            else:
                dic[I]=1
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


   
    

































