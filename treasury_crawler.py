# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 23:12:36 2018

@author: DongliangLu
"""

import sqlite3
import pandas as pd

mydb=sqlite3.connect("D:\\chromedownload\\doddfranktreasury.sqlite") 

cursor=mydb.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  
Tables=cursor.fetchall()  
print(Tables)


mydb.row_factory = sqlite3.Row
cursor.execute("select * from attendees")
rows = cursor.fetchall()

Treasury=pd.DataFrame(rows,columns=['attendee','topics','month','year','date','org','attendee hash'])
Treasury.to_csv("D:\\chromedownload\\Meeting_Treasury.csv")
