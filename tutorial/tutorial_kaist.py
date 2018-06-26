import pandas as pd
import numpy as np
import json
%pylab

import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False


## Parse json log
data = []
mydf = pd.DataFrame()

# to parse json files
with open('/Users/songhunhwa/Desktop/merged_file_p1.json') as f:
	for line in f:
		data.append(json.loads(line))

	# to convert json to pd dataframe
	for i in range(0, len(data)):
		df = pd.DataFrame.from_dict([data[i]])
		mydf = mydf.append(df)

## Preprocessing
cols = ["memNo", "sessionId", "timestamp", "screenName", "type", "event"]
df1 = mydf[cols].reset_index(drop=True).replace("", np.NaN)

df1['datetime'] = pd.to_datetime(df1.timestamp/1000, unit='s').dt.date.astype('datetime64[ns]')
df1.drop("timestamp", axis=1, inplace=True)

df1.info()

# daily log collection count
df1.datetime.value_counts()
df1.groupby("datetime")['sessionId'].count()
df1.groupby("datetime")['sessionId'].nunique()
df1.groupby("datetime")['sessionId'].size()

# Screen count
df1['screenName'].value_counts().order().plot(kind='barh', fontsize=9, figsize=(12,6))
plt.title("Screens that Frequently Shown by Users")
plt.grid(color='lightgrey', alpha=.5)
plt.xlabel("Frequency")

df1['event'].value_counts()


# Conversion Rate
total_session = df1.groupby("datetime")['sessionId'].nunique()
total_session

paid_session = df1.query("screenName == '/Ord/Track' and type == 'View'")\
				  .groupby("datetime")['sessionId'].nunique()
paid_session

cr = pd.concat([total_session, paid_session], axis=1)
cr.columns = ['total_session', 'paid_session']
cr['conv_rate'] = cr['paid_session'] / cr['total_session'] * 100

cr.conv_rate.fillna(0).plot(kind='line', rot=0, figsize=(8,5))
plt.title("The No. of the Total Session")
plt.grid(color='lightgrey', alpha=.5)
plt.xlabel("Day of April")


# Funnel 
key_screen = ['/Main', '/Shop', '/Shop/Menu', '/Ord', '/Ord/Payment', '/Ord/Track', '/Review']
df2 = df1[df1['screenName'].isin(key_screen) == True]
df2_gr = df2.groupby(["datetime", "screenName"])['memNo'].nunique().unstack()

df2_cols = df2_gr.columns.tolist()
df2_cols_re = [df2_cols[0]] + df2_cols[-2:] + df2_cols[1:5]

df2_re = df2_gr[df2_cols_re].fillna(0)
df2_re

# Screen path
top_screen = ['/Main', '/Shop', '/Shop/Menu', '/Ord', '/Ord/Payment', '/Ord/Track', '/Review', '/Search', '/Search/Result', '/Ord/History', '/Ord/Now']
df_top_screen = df1[df1['screenName'].isin(top_screen) == True]\
							   		 .query("type == 'View'")\
							  		 .drop_duplicates(subset=['datetime', 'sessionId', 'screenName'])\
							  		 .sort_values(['sessionId', 'datetime'])\
							  		 .groupby("sessionId")['screenName'].apply(lambda x: ', '.join(x))\
							  		 .reset_index()

df_top_screen.screenName.value_counts()[:20]

# Next screen after the goal
df_next = df1[df1['screenName'].isin(top_screen) == True]\
							   		 .query("type == 'View'")\
							  		 .drop_duplicates(subset=['datetime', 'sessionId', 'screenName'])\
							  		 .sort_values(['sessionId', 'datetime']).reset_index(drop=True)\
									 [['datetime', 'sessionId', 'screenName']]

main_next_list = []

for i in range(0, len(df_next)):
	if df_next.iloc[i, 2] == '/Main'\
		and i != len(df_next)-1\
		and df_next.iloc[i, 1] == df_next.iloc[i+1, 1]:
			main_next_list.append(i+1)

df_next.ix[main_next_list]['screenName'].value_counts()

# Text Processing
from konlpy.tag import Kkma, Hannanum, Twitter
from konlpy.utils import pprint

#-*- coding: utf-8 -*-
#import sys  
#reload(sys)
#sys.setdefaultencoding('utf8')

shop_review = pd.read_csv("/Users/songhunhwa/Desktop/review_text.csv", encoding='utf-8')

twitter = Twitter()

word_list = []
for i in range(0, len(shop_review.review)):
	w = [x[0] for x in twitter.pos(shop_review.review.ix[i], stem=True) if (("Adjective" in x) or ("Verb" in x))]
	word_list.append(w)

word_list_pd = pd.Series([y for x in word_list for y in x])
word_list_pd.value_counts()[:30].order().plot(kind='barh', figsize=(10,8))


# with Scikit learn
from sklearn.feature_extraction.text import CountVectorizer

vect = CountVectorizer().fit(word_list_pd)
count = vect.transform(word_list_pd).toarray().sum(axis=0)
pprint(zip(vect.get_feature_names(), count))

#vect.vocabulary_





