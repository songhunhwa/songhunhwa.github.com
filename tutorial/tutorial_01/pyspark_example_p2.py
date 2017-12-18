
# import modules
from pyspark.sql import SQLContext
from pyspark.sql.functions import *
import pandas as pd
import numpy as np

sc = SparkContext()
sqlContext = SQLContext(sc)

# read the csv with library
df = sqlContext.read.format('com.databricks.spark.csv')\
					.options(header='true', inferSchema='true')\
					.load('/Users/woowahan/Documents/Python/DS_Ext_School/tutorial_01/doc_use_log.csv')\
					.cache()

df.printSchema()
df.count()

# convert the df to tmp table (as if it's in database)
df.registerTempTable("df_tmp")

# extract data from table with sql
df1 = sqlContext.sql("select ismydoc, actiontype, sessionid, datetime from df_tmp where ismydoc = true")

# other sql examples
sqlContext.sql("select datetime, count(1) from df_tmp group by datetime order by datetime").show()
sqlContext.sql("select count(distinct sessionid) as session_cnt from df_tmp where documentposition = 'MYPOLARISDRIVE' group by ext having count(distinct sessionid) ").show()

print(df.count())
print(df1.count())

## Lazy Execution
df2 = sqlContext.sql("select * from df_tmp")

df2_pdf = df2.select("sessionid", "ext").filter(" ext == 'PDF' or ext = 'DOC'").dropDuplicates().cache()
df2.fil.distinct().count()

df2_min_date = df2.groupby("sessionid").agg(min("datetime").alias("min_date"))
df2_min_date.show()

df2_join = df2_pdf.join(df2_min_date, "sessionid", "left")
df2_join.show()

df2_join1 = df2_join.groupby("min_date", "ext").agg(count("sessionid").alias("cnt"))

df2_join1.describe().show()

# Pandas
df2_pd = df2.toPandas()
df2_pd.groupby("ext")['sessionid'].count().sort_values(ascending=False)
df2_pd['ext'].value_counts()


# other functions
fillna()
dropDuplicates()
drop()
distinct()
countDistinct()
withColumn()
withColumnRenamed()
pivot()
sort()
collect_list()
collect_set()
get_json_object()
from_unixtime()
to_date()
sample(False, 0.1, 123) 
cube()
cache()

more reference: http://spark.apache.org/docs/latest/api/python/pyspark.sql.html