
import pandas as pd 
import numpy as np 

df = pd.read_csv("cheatsheet.csv", encoding = "ISO-8859-1",na_filter=False)

df = pd.DataFrame(df)

list1=[85920333,95920028,90909021,80909935]

df.loc[df['GROUPER'].isin(list1)," Ownership"] = 'No Ownership'
df.loc[df['GROUPER'].isin([90111007]),'Tax Id #'] = '901034858'
df.loc[df['GROUPER'].isin([90111007]),'Effective Date of Original Contract'] = '1.1.2011'
df.loc[df['GROUPER'].isin([90111007]),'Effective Date of Grouper'] = '1.1.2012'

writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()
