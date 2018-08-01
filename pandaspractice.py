# Basic Pandas Knowledge

import pandas as pd 
import numpy as np 

df = pd.read_csv("cheatsheet.csv", encoding = "ISO-8859-1",na_filter=False)

df.shape #Give the dimension (rows,columns)

df.head() #see top 5 rows of data 

df.dtypes # datatype of each variable(column)

df.columns # column names

df.info() # provide if we have any null in data


## Advanced Indexing

# df.iloc[0,4]: Select based on integer location, where 0= 1st row and the bracket indicate a closed ending number (not included)
df.iloc[0,3]   # Row 0, column 3 = PCP Center Selection - ORL NR
df.iloc[562,10] # Row 562, column 10 = LR
df.iloc[:3] # Row 1 to 3, with all the columns

df.iloc[1:3,3] # Row 2-3, column 2-3
#     CONSOLIDATED NAME         CONSOLIDATED MARKET
#1  PCP CENTER SELECTION  PCP CENTER SELECTION - ORL

df.iloc[1:3,1:3]  # Taking 0,1,2 as row 1,2,3 and 3 is closed paranthese.
df.iloc[:3,1]
#    GROUPER     CONSOLIDATED NAME         CONSOLIDATED MARKET
#0    30980  PCP CENTER SELECTION  PCP CENTER SELECTION - ORL
#1    32394  PCP CENTER SELECTION  PCP CENTER SELECTION - ORL
#2    32395  PCP CENTER SELECTION  PCP CENTER SELECTION - TAM


# loc: Select based on name of the column, cap sensitive. Row remain numbered.

df.loc[1:2,'GROUPER':'CONSOLIDATED NAME'] # Loc gives us row 2 AND 3 


df.loc[1,['GROUPER',"CONSOLIDATED NAME"]] # It's like a transpose, columns become rows 

#GROUPER                     32394
#CONSOLIDATED NAME    PCP CENTER SELECTION
#Name: 1, dtype: object


##  Conditional select

df[(df.iloc[:,6]=='Alicia Ray')].iloc[0:5]  #If a column has two words, use integer location to get it
df[(df.MARKET == 'ORL')].iloc[0:20] #Select the first 20MSO with location in ORL
df[(df.MARKET == 'TAM') | (df.iloc[:,6]=='Alicia Ray')].iloc[:3] #Select where market=TAM or F.A= Alicia, () are important 
df.loc[:,(df < 2).all()][:3]  # all rows with the column that has string less than 2 or int<2

sum((df.Survived != 0) & (~(df.Pclass == 3)) )

#  filter all rows which have Age > Passenger ID
df.query('Age > Passenger')  DataFrame.query(string expr, inplace=False, **kwargs)
 
# filter only sex and age columns (first 2 rows)
DataFrame.filter(items=None, like=None, regex=None, axis=None)
df.filter(items=['GROUPED NAME','REGION'])[:2] # Filter 2 columns by name and the first 2 rows.

# filter only 0 and 5 row index
df.filter(items=[0,5], axis=0)  #axis is the column #, and items is what row we want to pick
# GROUPER     CONSOLIDATED NAME         CONSOLIDATED MARKET  \
#0    30980  PCP CENTER SELECTION  PCP CENTER SELECTION - ORL
#5    32473  PCP CENTER SELECTION  PCP CENTER SELECTION - JAX

#isin
#Filter rows of column based on list of multiple values
list1=[85920333,95920028,90909021,80909935]
df.loc[df['GROUPER'].isin([85920333,95920028,90909021,80909935]),"Humana Ownership"] = 'No Humana Ownership'
df.loc[df['GROUPER'].isin(list1),"Humana Ownership"] = 'No Humana Ownership'


#Setting/ Resetting Index
#Setting and resetting index are important when we merge/groupby 2 dataframe and want to do further analysis on new dataframe. A dataframe with repeated indexes can cause problems in filtering.

#setting Index, where the data is set according to the column data
df.set_index(['MARKET'])[:2] 

#         GROUPER     CONSOLIDATED NAME         CONSOLIDATED MARKET  \
#MARKET
#ORL       30980  PCP CENTER SELECTION  PCP CENTER SELECTION - ORL
#ORL       32394  PCP CENTER SELECTION  PCP CENTER SELECTION - ORL

df.set_index('MARKET','Type')[:2] #Multiple columns as index

df_reset= df.set_index(['MARKET']) # To see the value of the first index row in MARKET
df_reset.reset_index()[:1] #can reset index back to 0, and Market become a column 

#rename() 
Renaming column names or row indexes of dataframe. Default is index
df.rename(columns={'GROUPER':'Testing', "MARKET":'Testing123'})[:2]


# unique: Show the unique value of the column
df.iloc[:,1].unique() # unique value of consolidated name

# check for duplicated value

sum(df.GROUPER.duplicated()) # value of 0 implies no duplication
drop_duplicates() # use when drop duplicates

# unique combination of mutiple columns

df.loc[:,['MARKET','LOB']].drop_duplicates()
#                    MARKET LOB
#0                   ORL  HMO
#2                   TAM  HMO
#4                   JAX  HMO

#GROUPING DATA: Group by some columns and do aggregate to calculate mean, coun, ..etc

df.groupby(by = ['LOB']).count()

# can group by indexes also by using levels= 
# useful when we have multindexes
# can use agg function with lambda func

df_index = df.set_index(['Sex', 'Pclass'])
df_index.groupby(level=[0,1]).agg({'Fare': lambda x: sum(x)/len(x), # this is also just mean actually
                                  'Age' : np.mean})

		        Fare	Age
Sex 	Pclass		
female	1	106.125798	34.611765
	    2	21.970121	28.722973
	    3	16.118810	21.750000
male	1	67.226127	41.281386
	    2	19.741782	30.740707
	    3	12.661633	26.507589
df_index.groupby(level=[0,1]).transform(lambda x: sum(x)/len(x)).head() # transform will apply for all rows


df.dropna(axis=0, how='any').shape #drops all columns=NA

df.fillna(np.mean)[:1] replace NA with the mean of the column, or it can be any value 


# inner join when both table have that key (like sql), 
data1.merge(data2, how='inner', on='x1')
# join over axis=0, i.e rows combine 
# also adds all columns with na

pd.concat([data1, data2], axis=0)

# index = new index, columns = new_columns, values = values to put
df.pivot(index='Sex', columns = 'PassengerId', values = 'Age')

# apply -> apply function over df
# apply_map -> apply function elementwise (for each series of df. think of column wise)
In [83]:
# function squares when type(x) = float, cubes when type(x) = int, return same when other
f = lambda x: x**2 if type(x) == float else x**3 if type(x) == int else x
In [84]:
# whole series is passed
df.Fare.apply(f)[:3]


str
Working with string format in pandas series/df
We can do:
• str.upper()/lower() to convert string into upper or lower case
• str.len() to find the length of sting
• str.strip()/lstrip()/rstrip() to strip spaces
• str.replace() to replace anything from string
• str.split() to split words of string or using some other delimiter
• str.get() to access elements in slit list
• str.resplit() spit in reverse order of string based on some delimiter
• str.extract() extract specific thing from string. alphabet or number
Let's see how to use all that in pandas series. Keep in mind pandas DataFrame has no attribute called str and works on Series object only. So, grab column of df, then apply str


# splits strings in each row over whitespaces ()
# expand=True : expand columns
# pat = regex to split on
df.Name.str.split(pat=',',expand=True).head().rename(columns={0:'First_Name', 1: 'Last_Name'})


In [91]:
# replace Mr. with empty space
df.Name.str.replace('Mr.', '').head()
