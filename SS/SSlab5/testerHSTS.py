import random
import requests 
import pandas as pd

"""
['S/no.', 'Website']
1	google.com
2	youtube.com
3	facebook.com
4	baidu.com
5	yahoo.com
6	instagram.com
7	bilibili.com
"""

siteNum = random.randint(0, 50)

print(siteNum)


headers = ['S/no.', 'Website']
sourcepath = 'D:/kht/10_MSSD/10.4_T2/51.502 SS/L5ss/top-50.csv'

#df = pd.read_csv(sourcepath, header = None)

# Below add headers. The auto data source is not having header. It is in another file
df = pd.read_csv(sourcepath)
df.columns=headers
# print(df.head(2))
print(df)
print('\nOutput of df.iloc Single Bracket[0,1], getting data at the specific location\n')
print(df.iloc[0,1])

print('\nOutput of df.iloc Single Bracket[0,0], getting data at the specific location\n')
print(df.iloc[0,0])

print('\nOutput of df.iloc Single Bracket[6,1], getting data at the specific location\n')
print(df.iloc[siteNum,1])
print(type(df.iloc[siteNum,1]))
