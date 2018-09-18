# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 19:43:07 2018

@author: DongliangLu
"""

import sqlite3
import pandas as pd

mydb=sqlite3.connect("D:\\chromedownload\\doddfrankfed.sqlite") 

cursor=mydb.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  
Tables=cursor.fetchall()  
print(Tables)


mydb.row_factory = sqlite3.Row
cursor.execute("select * from AttendeeTable1")
rows = cursor.fetchall()

Treasury=pd.DataFrame(rows,columns=['category','date','affiliation','attendee_name','name'])
Treasury.to_csv("D:\\chromedownload\\Meeting_Fed.csv")