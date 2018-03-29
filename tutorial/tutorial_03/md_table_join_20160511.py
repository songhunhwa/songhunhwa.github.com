from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import *
import pandas as pd
import numpy as np
from datetime import datetime
import time

sc.stop()

# [ID list]
mydata_lc = pd.read_csv("liam/mydata_lc.csv")

mydata_lc.info()
mydata_lc.describe()
mydata_lc.shape

pd.value_counts(mydata_lc.keyset)

# [API count] call table
count = sqlContext.sql("SELECT iduser, SUM(viewCount) AS viewCount, SUM(editCount) AS editCount, SUM(shareCount) AS shareCount, SUM(searchCount) AS searchCount, SUM(coworkCount) AS coworkCount FROM mart.tbActiveApiCount WHERE day>='2016-04-02' AND day<='2016-05-02' GROUP BY iduser")

# filter view = 0 
count_df = count.filter("viewCount > 1")

# to pd df
count_lc = count_df.toPandas() 

count_lc.info()
count_lc.describe()
count_lc.shape
count_lc.iduser = pd.to_numeric(count_lc.iduser, errors='raise')
count_lc.to_csv('liam/count_lc.csv')

####count_lc_num = count_lc.iduser.convert_objects(convert_numeric=True)

# file management
fm_lc = pd.read_csv("liam/fm_lc.csv")

fm_lc.info()
fm_lc.describe()
fm_lc.shape

# merge id & count & fm (names were mixed up)
# join step 1
mydata_cnt = pd.merge(mydata_lc, count_lc, on='iduser', how='left')

mydata_cnt.head()
mydata_cnt.info()
mydata_cnt.describe()
mydata_cnt.shape

# # join step 2
mydata_cnt_fm = pd.merge(mydata_cnt, fm_lc, on='iduser', how='left')

mydata_cnt_fm.head()
mydata_cnt_fm.info()
mydata_cnt_fm.describe()
mydata_cnt_fm.shape

# [visit count] call table
vis = sqlContext.sql("SELECT iduser, COUNT(DISTINCT day) as visdays FROM mart.tbDailyUserInfo WHERE day>='2016-04-02' AND day<='2016-05-02' GROUP BY iduser")
vis_df = vis.filter("visdays > 1")

vis_lc = vis_df.toPandas()
vis_lc.iduser = pd.to_numeric(vis_lc.iduser, errors='raise')
vis_lc.head(n=10)

vis_lc.info()
vis_lc.describe()
vis_lc.shape

# join step 3
mydata_cnt_fm_vis = pd.merge(mydata_cnt_fm, vis_lc, on='iduser', how='left')

mydata_cnt_fm_vis.info()
mydata_cnt_fm_vis.head(n=10)

mydata_cnt_fm_vis.to_csv('liam/mydata_cnt_fm_vis.csv')

mydata_cnt_fm_vis = mydata_cnt_fm_vis.drop('key_x', 1)
mydata_cnt_fm_vis = mydata_cnt_fm_vis.drop('key_y', 1)

mydata_cnt_fm_vis.rename(columns={'keyset': 'group'}, inplace=True)


# BM Action
act = sqlContext.sql("SELECT iduser, SUM(openCount) AS openCount, SUM(saveCount) AS saveCount, SUM(exportCount) AS exportCount, SUM(viewTraffic) AS viewTraffic, SUM(editTraffic) AS editTraffic, SUM(exportTraffic) AS exportTraffic FROM mart.tbBMAction WHERE day>='2016-04-02' AND day<='2016-05-02' GROUP BY iduser")
act_df = act.filter("openCount > 1")

act_lc = act_df.toPandas()
act_lc['traffic'] = act_lc['viewTraffic'] + act_lc['editTraffic'] + act_lc['exportTraffic']

act_lc.info()

# join step 4

mydata_cnt_fm_vis_act = pd.merge(mydata_cnt_fm_vis, act_lc, on='iduser', how='left')
mydata_cnt_fm_vis_act.head()

mydata_cnt_fm_vis_act.to_csv('liam/mydata_cnt_fm_vis_act.csv')


### Regist info
reg = sqlContext.sql("SELECT * FROM mart.tbRegistUserInfo WHERE day='2016-05-10' LIMIT 15")
reg_lc = reg.toPandas()

datetime.fromtimestamp(reg_lc['datetime'])
reg_lc['datetime'].strftime('%Y-%m-%d')

info



# # reg_lc['datetime'] = datetime.datetime.fromtimestamp('datetime').strftime('%Y-%m-%d %H:%M:%S')
# # reg_lc.head()


