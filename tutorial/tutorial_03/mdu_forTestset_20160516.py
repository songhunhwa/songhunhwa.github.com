ssh -i C:/Users/liam.song/Desktop/EMR_California.pem -NL 8888:localhost:62080 hadoop@ec2-52-53-223-130.us-west-1.compute.amazonaws.com

import sys
import os
sys.path.append('/usr/lib/spark')
sys.path.append('/usr/lib/spark/python/lib/py4j-0.9-src.zip')
sys.path.append('/usr/lib/spark/python')
from pyspark import SparkContext
from pyspark.sql import HiveContext
from pyspark import SparkConf
os.environ["SPARK_HOME"] = "/usr/lib/spark"
conf = SparkConf().setMaster('local').setAppName('a')
sc = SparkContext(appName = "test")
sqlContext = HiveContext(sc)

from time import strftime
from datetime import datetime

import pandas as pd
import numpy as np

sc.stop()

#################################################################################
# how to change datetime as in pandas
# df['datetime'] = df['datetime'].astype(int) # if not int
# df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d')

mdu = sqlContext.sql("SELECT * FROM mart.tbMultiDeviceUserInfoAccum WHERE day='2016-05-15'")
mdu_lc = mdu.toPandas()

mdu_lc['timemdu'] = pd.to_datetime(mdu_lc['timemdu'], unit='s')
# datetime.fromtimestamp(mdu_lc['datetime']).strftime('%Y-%m-%d')


#################################################################################

# read table
acuser = sqlContext.sql("SELECT * FROM mart.tbDailyUserInfo WHERE day>='2016-04-02' AND day<='2016-05-02'")
sam_acuser = acuser.sample(False, 0.03)

sam_acuser.show()
sam_acuser.count() # 1079040
sam_acuser.describe.show()

acuser_id = sam_acuser.select('iduser').collect()
type(acuser_id) # list

acuser_id_df = pd.DataFrame(acuser_id, columns=['iduser']) # conver to pandas df
dc_acuser_id = acuser_id_df.drop_duplicates(['iduser'])
type(dc_acuser_id) # df pandas
len(dc_acuser_id) # 923896

# add mdu columns to acuser_lc
mdu = sqlContext.sql("SELECT * FROM mart.tbMultiDeviceUserInfoAccum WHERE day='2016-05-17'")

mdu_id = mdu.select(['iduser', 'mdutype']).collect()
mdu_id_lc = pd.DataFrame(mdu_id, columns=['iduser', 'mdutype'])

mdu_id_lc['key'] = 1
mdu_id_lc['keyset'] = 'mdu'

acuser_mdu = pd.merge(dc_acuser_id, mdu_id_lc, on='iduser', how='left')

acuser_mdu.to_csv('liam/acuser_mdu.csv') 
acuser_lc = pd.read_csv("liam/acuser_mdu.csv", index_col=0)


# read mydata_lc.csv for inner join
mydata_lc = pd.read_csv("liam/mydata_lc.csv") #900908
mydata_lc.iduser = pd.to_numeric(mydata_lc.iduser, errors='raise')


# merge
inner_merged = pd.merge(acuser_lc, mydata_lc, on='iduser', how='inner') # ZERO, nothing duplicated
inner_merged['key'] = 99 # crossed code
inner_merged_id = pd.DataFrame(inner_merged, columns=['iduser', 'key'])


tb_merged = pd.merge(acuser_lc, inner_merged_id, on='iduser', how='left')
tb_merged_sub = tb_merged[tb_merged.key_y != 99] 

tb_merged_sub.info()
tb_merged_sub.describe()
tb_merged_sub.shape

tb_merged_sub = tb_merged_sub.drop(['key_x', 'key_y'], 1)
tb_merged_sub.to_csv('liam/test_set.csv')


# random sampling
import random
rows = random.sample(test_set.index, 200000)
sam_testset = test_set.ix[rows]


sam_testset_id.rename(columns={'keyset': 'group'}, inplace=True)
sam_testset_id.group = sam_testset_id.group.replace(np.nan, 'sdu')

sam_testset_id.to_csv('liam/sam_testset_id.csv')
sam_testset_id = pd.read_csv("liam/sam_testset_id.csv", index_col=0)


#### join other tables


# [API count] call table
count_lc = pd.read_csv("liam/count_lc.csv")

# file management
fm_lc = pd.read_csv("liam/fm_lc.csv")


# [visit count] call table
vis = sqlContext.sql("SELECT iduser, COUNT(DISTINCT day) as visdays FROM mart.tbDailyUserInfo WHERE day>='2016-04-02' AND day<='2016-05-02' GROUP BY iduser")
vis_df = vis.filter("visdays > 1")

vis_lc = vis_df.toPandas()
vis_lc.iduser = pd.to_numeric(vis_lc.iduser, errors='raise')

vis_lc.info()
vis_lc.describe()
vis_lc.shape

vis_lc.to_csv('liam/vis_lc.csv')

# BM Action
act = sqlContext.sql("SELECT iduser, SUM(openCount) AS openCount, SUM(saveCount) AS saveCount, SUM(exportCount) AS exportCount, SUM(viewTraffic) AS viewTraffic, SUM(editTraffic) AS editTraffic, SUM(exportTraffic) AS exportTraffic FROM mart.tbBMAction WHERE day>='2016-04-02' AND day<='2016-05-02' GROUP BY iduser")
act_df = act.filter("openCount > 1")

act_lc = act_df.toPandas()
act_lc['traffic'] = act_lc['viewTraffic'] + act_lc['editTraffic'] + act_lc['exportTraffic']

act_lc.info()
act_lc.describe()
act_lc.shape

act_lc.to_csv('liam/act_lc.csv')


### merge id & count & fm (names were mixed up)

test_id = sam_testset_id

# join step 1
test_cnt = pd.merge(test_id, count_lc, on='iduser', how='left')

test_cnt.head()
test_cnt.info()
test_cnt.describe()
test_cnt.shape

# join step 2
test_cnt_fm = pd.merge(test_cnt, fm_lc, on='iduser', how='left')

test_cnt_fm.head()
test_cnt_fm.info()
test_cnt_fm.describe()
test_cnt_fm.shape

# join step 3
test_cnt_fm_vis = pd.merge(test_cnt_fm, vis_lc, on='iduser', how='left')

test_cnt_fm_vis.head()
test_cnt_fm_vis.info()
test_cnt_fm_vis.describe()
test_cnt_fm_vis.shape

# join step 4
test_cnt_fm_vis_act = pd.merge(test_cnt_fm_vis, act_lc, on='iduser', how='left')

test_cnt_fm_vis_act.head()
test_cnt_fm_vis_act.info()
test_cnt_fm_vis_act.describe()
test_cnt_fm_vis_act.shape

test_cnt_fm_vis_act = test_cnt_fm_vis_act.drop(['Unnamed: 0', 'key'], 1)

test_cnt_fm_vis_act.to_csv('liam/testset.csv')


## Regist info
# reg = sqlContext.sql("SELECT * FROM mart.tbRegistUserInfo WHERE day='2016-05-10' LIMIT 15")
# reg_lc = reg.toPandas()
# datetime.fromtimestamp(reg_lc['datetime'])
# reg_lc['datetime'].strftime('%Y-%m-%d')
