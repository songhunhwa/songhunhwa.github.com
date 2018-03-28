---
title: "1회차 Part2: 데이터 수집 및 처리 시스템 소개"
layout: post
author: songhunhwa
---

### 목적
- 1강 Part1(분석실무에 대한 이해) 내용중 분석 시스템 환경/툴 및 개념에 대해 학습한다.
- JSON 형태의 로그 데이터를 Parsing 및 전처리하는 실습을 진행한다.

### 목차
1. Apache Spark & Modules 소개
2. AWS 소개
2. 클라이언트 로그 설계 사례
3. (실습) Json 및 Text 형태의 로그 데이터 Parsing
4. (실습) SQL 및 Numpy, Pandas를 통한 전처리

### Apache Spark & Modules 소개
#### 분석 환경
분석 환경은 주로 엔지니어 및 회사 고유의 상황에 따라 결정된다. 분석가는 환경적/구조적 특성과 제한점 등 여러 사항을 고려하여 분석을 진행한다. 특히 데이터 수집 과정을 분석 목적에 맞게 최적화 하는 등의 목적을 위해 분석가가 환경 및 구조에 관여하기도 한다. 물론, 분석가가 주도적으로 처음부터 환경을 설정하고 구조를 쌓아올라가는 경우도 있지만 이는 일반적인 상황이라고 보기 어렵다. 
    
분석가가 좋은 성과를 내기 위해서는 **분석 환경을 잘 이해/활용하고 때로는 (분석 관점에 맞게) 개선점을 엔지니어에게 전달**하는 등 역할이 필요하다. 따라서 (실무는 엔지니어가 진행하더라도) 환경/시스템적 요소에 대한 이해와 지속적인 관여 역시 분석가의 역할이기도 하다.    
          
#### [스파크](https://spark.apache.org/) 소개
최근 비정형 데이터의 생성과 매우 큰 사이즈 등의 이슈로 기존 RDBS에서 하둡/스파크를 도입하는 추세이다. 비록 RDBS만큼 즉각적 생성/수정/변경 등은 어렵지만, Spark나 하둡을 이용할 경우 분산 저장 및 처리를 통해 빠른 분석 진행이 가능하다. 최근에는 하둡 보다 **분석 친화적인 스파크**를 주로 사용해 분석하는 추세이다. 스파크가 Pyspark이나 SparkR 같은 다양한 분석 API를 제공하고 있기 때문이다. 참고로 하둡은 Java, Spark는 원래 스칼라 기반이다.

<img src="/img/lecture/spark_frame.png" width="65%">

Source: [Nimisha Sharath Sharma](https://www.linkedin.com/pulse/apache-spark-scala-via-python-nimisha-sharath)

#### 스파크 RDD, DataFrame, Lazy execution
스파크에서 다루는 주요 데이터 타입은 **RDD**(Resilient Distributed Datasets)와 **DataFrame**이다. 기존 하둡에서는 디스크에서 데이터 I/O가 발생하는 반면, 스파크는 RAM에서 발생하게 설정할 수 있으므로 속도에서 비약적인 차이가 발생한다. 최근에는 RDD보다 DataFrame을 이용하는 추세이며(RDBS의 테이블이나 Pandas Dataframe과 유사하기 때문), Spark의 특징인 **Lazy execution**을 통해 보다 효율적인 처리/분석이 가능하다.
     
Lazy Execution은 함수를 **Transform, Action** 으로 구분해 Action 일 경우에만 실제 실행이 발생하는 것을 의미한다. 매번 결과를 갖고 오지 않고, 필요한 경우에만 RAM을 통해 데이터 I/O가 발생하므로 분석 작업 속도가 매우 높아진다. Spark에서 데이터 분석을 하는 경우, 매우 큰 사이즈의 데이터를 다루는 경우가 많아 이러한 매커니즘은 매우 중요한 장점으로 작용한다. (다행히 Transform 단계라도 에러를 내보내므로 Action 단계에서 제대로 결과가 나왔는지 걱정할 필요는 없다)     

**RDD**
 - Distribute collection of JVM objects
 - Funtional Operators (map, filter, reduceByKey, ect)

<img src="/img/lecture/spark_rdd.png" width="65%">

Source: [Research Computing](http://researchcomputing.github.io/meetup_spring_2014/python/spark.html)

**DataFrame**
 - Distribute collection of Row objects
 - Expression-based operations and UDFs
 - Logical plans and optimizer
 - Fast/efficient internal reprenstations
 
<img src="/img/lecture/spark_df.png" width="70%">

Source: [Duchess france](http://www.duchess-france.org/starting-with-spark-in-practice/)

**Lazy Execution**
 - Transfrom: `filter`, `select`, `drop`, `join`, `dropDuplicates`, `distinct`, `withColumn`, `pivot`, `get_json_object`, `sample`
 - Action: `count`, `collect`, `show`, `head`, `take`

<img src="/img/lecture/spark_le.png" width="70%">

Source: [Birendra Kumar Sahu](http://www.grroups.com/blog/how-spark-deconstructed)

**Spark 실습**
 - [Download Page](http://spark.apache.org/downloads.html)
 - [Github Page for Tutorial](https://github.com/songhunhwa/songhunhwa.github.com/tree/master/tutorial/tutorial_01)
 - SparkContext 생성
 - DataFrame 생성 및 추출
 - 전처리 및 분석

```python
# import modules
from pyspark.sql import SQLContext
from pyspark.sql.functions import *

sc = SparkContext()
sqlContext = SQLContext(sc)

# read the csv with library
df = sqlContext.read.format('com.databricks.spark.csv')\
					.options(header='true', inferSchema='true')\
					.load('/Users/woowahan/Documents/Python/DS_Ext_School/tutorial_01/doc_use_log.csv')

# convert the df to tmp table (as if it's in database)
df.registerTempTable("df_tmp")

# extract data from table with sql
df1 = sqlContext.sql("select ismydoc, actiontype, sessionid, datetime from df_tmp where ismydoc = true")

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
```
#### 스파크 Modules 
스파크가 최근에 각광을 받게 된 배경에는 스파크가 제공하는 모듈도 영향을 미쳤다. 스파크는 분산처리프레임 위에 **Spark Streaming, SparkSQL, MLlib, GraphX**와 같은 모듈을 제공하여 실시간 수집부터 데이터 추출/전처리, 머신러닝 및 그래프 분석까지 하나의 흐름에 가능하도록 개발되었다. 각 모듈의 특성을 살펴보자.

 - [Spark SQL](https://spark.apache.org/sql/): Spark Wrapper 함수에 SQL 쿼리를 넣어 추출/전처리/분석이 쉽게 가능하도록 지원
 - [MLlib](https://spark.apache.org/mllib/): 머신러닝 알고리즘 제공 [(코드 예시)](https://github.com/songhunhwa/MachineLearning_Pyspark)
 - [Spark Streaming](https://spark.apache.org/streaming/): 실시간 데이터 처리
 - [GraphX](https://spark.apache.org/graphx/): 그래프 분석 라이브러리
 
 위 4개의 모듈 중에 분석가가 많이 사용하는 것은 Spark SQL과 Mllib이다. 아래 예시 코드를 보자.

```python
## 데이터 추출 및 전처리 with Spark SQL
from pyspark.sql.funtions import *

df = spark.sql("select * from mart.table").select("date", "mem")
df1 = df.filter("date is not null").groupby("date").agg(count("mem").alias("mem_cnt")

## 모델 생성 with MLlib
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler, StandardScaler
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression

strIdx = StringIndexer(inputCol = "student", outputCol = "studentIdx")
encode = OneHotEncoder(inputCol = "studentIdx", outputCol = "studentclassVec")

stages = [strIdx, encode, label_StrIdx]
inputs = ["studentclassVec", "incomeScaled", "balanceScaled"]
assembler = VectorAssembler(inputCols = inputs, outputCol = "features")
stages += [assembler]

pipelineModel = pipeline.fit(df)
dataset = pipelineModel.transform(df)

pipeline = Pipeline(stages = stages)

(train, test) = dataset.randomSplit([0.7, 0.3], seed = 14)
lr = LogisticRegression(labelCol = "label", featuresCol = "features", maxIter=10)

lrModel = lr.fit(train)
predictions = lrModel.transform(test)
predictions.show()

```

Source: [Songhunhwa's Github](https://github.com/songhunhwa/MachineLearning_Pyspark)

### AWS 소개
데이터를 수집하고 저장, 처리 및 분석하는 일련의 과정을 직접 구현하기에 많은 인력과 자원/시간이 소모된다. 이를 쉽게 가능하도록 클라우드 플랫폼 솔루션을 제공하는 것이 [AWS(Amazon Web Service)](https://aws.amazon.com/ko/big-data/)이다. 사용량 비례 과금 방식으로 잘 설계된 저장소와 서버 등 일련의 플랫폼을 저렴하게 사용할 수 있는 것이 가장 큰 장점이다.
    
분석가의 입장에서 가장 유용한 서비스는 [EMR](https://aws.amazon.com/ko/emr/)이다. EMR은 Spark, Hadoop, Presto, HBase 등 분석에 유용한 분산프레임워크를 제공한다. 또 Amazon S3 및 Amazon DynamoDB와 같은 저장소와 호환되므로 데이터 저장/입출력/추출/분석 등이 효율적으로 진행된다. 실무에서의 분석은 로컬에서 이뤄지지 않고 Amazon EMR Cluster를 띄워 사용당 과금을 하며, 서버에서 진행된다.     

<img src="/img/lecture/aws_frame.png" width="70%">

Source: [AWS](https://aws.amazon.com)

### 로그 정의/설계
로그 데이터는 최근 사용자의 사용성 및 행동 패턴을 확인하거나 유저 클러스터링, 모델링 등 다양한 목적으로 사용되는 행동 기반 데이터이다. 로그는 설문과 같은 사용자 응답 및 기억에 의존하는 데이터 수집 방법 대비, 행동을 정확하게 파악/예측할 수 있는 장점이 있다. 또 RDB의 결과론적인 데이터와 달리 특정 결과에 이르는 과정과 흐름을 상세히 파악할 수 있어, 서비스를 개선하는 데 매우 유용한 자료이다. 대신 데이터 용량이 크기 때문에 스토리지 관련 비용/리소스가 발생하고, JSON, CSV, TSV와 같은 비정형 텍스트 형태이므로 기존 RDB와는 다른 수집/처리 시스템과 전문 인력이 요구된다는 단점을 가지고 있다. 
    
분석가의 역할 중에 로그 정의 및 설계가 중요한 역할이다. 분석가는 산재된 로그를 분석 목적에 맞게 포멧을 정리하고 로깅할 항목을 우선순위에 맞게 정하는 역할을 한다. 또 로그 발생시 수집할 필드명과 값의 이름을 정의하고 설계하는 업무를 맡는다. 실제 데이터 수집/처리시 정의한 대로 로그가 쌓이므로, 이 단계는 매우 중요한 단계라고 할 수 있다. 더불어 쌓인 로그의 데이터 퀄리티를 관리하는 역할 역시 분석가의 몫이다.

#### 로그 정의 예시
최근 로그의 형태는 대부분 [JSON(JavaScript Object Notation)](https://www.w3schools.com/js/js_json_intro.asp)이다. Pandas의 Dictionary와 거의 유사하게 Key, Value로 구성되어 있으며, Hierchial 구조를 가질 수 있다. 분석가는 로그 송출시 Json의 Key와 Value에 들어갈 값을 정한다.

```JSON
{
 "memid": "int", 
 "sessionid": "int", 
 "ver": "float",
 "screen": "Intro",
 "event": "View",
 "area": "Begin",
 "group": "A",
 "params": {
            "isGuest": "Bool", 
            "UserType": "string"
            }
}
```
### [실습](https://github.com/songhunhwa/songhunhwa.github.com/tree/master/tutorial/tutorial_01)
- JSON Client Log Parsing with JSON Library
- 데이터 추출 with SQL, Pandas Dataframe


 

