# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 22:15:46 2018

@author: DongliangLu
"""

#
import pandas as pd
import xml.etree.cElementTree as et
 
add=r"C:\Users\DongliangLu\Desktop\2018_1_1_1.xml"
parsedXML = et.parse( add )

#for node in parsedXML.getroot():
    node=parsedXML.getroot()[-1]
    #attribute in filing can use this format
    period=node.attrib.get('Period')
    print(period)
    type_=node.attrib.get('Type')
    print(type_)
    
    #for content in second small nodes, use find first
    node.find("Registrant").attrib.get("Address")
    node.find("Issues/Issue").attrib.get("xmlns")
    node.find("Issues/Issue").attrib.get("SpecificIssue")
    #for child root has many same names
    for i in node.iter("Issue"):
        print(i.get("SpecificIssue"))
    
    attrib.get("Issue")
    a=node.find("Issues").get("Issue")
    










