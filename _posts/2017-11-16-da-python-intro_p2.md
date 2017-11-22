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
#### 분석 환경의 이해는 중요 
분석 환경은 주로 엔지니어 및 회사 고유의 상황에 따라 결정된다. 분석가는 환경적/구조적 특성과 제한점 등 여러 사항을 고려하여 분석을 진행한다. 특히 데이터 수집 과정을 분석 목적에 맞게 최적화 하는 등의 목적을 위해 분석가가 환경 및 구조에 관여하기도 한다. 물론, 분석가가 주도적으로 처음부터 환경을 설정하고 구조를 쌓아올라가는 경우도 있지만 이는 일반적인 상황이라고 보기 어렵다. 
    
분석가가 좋은 성과를 내기 위해서는 **분석 환경을 잘 이해/활용하고 때로는 (분석 관점에 맞게) 개선점을 엔지니어에게 전달**하는 등 역할이 필요하다. 따라서 (실무는 엔지니어가 진행하더라도) 환경/시스템적 요소에 대한 이해와 지속적인 관여 역시 분석가의 역할이기도 하다.    
          
#### 스파크 소개
최근 비정형 데이터의 생성과 매우 큰 사이즈 등의 이슈로 기존 RDBS에서 하둡/스파크를 도입하는 추세이다. 비록 RDBS만큼 즉각적 생성/수정/변경 등은 어렵지만, Spark나 하둡을 이용할 경우 분산 저장 및 처리를 통해 빠른 분석 진행이 가능하다. 최근에는 하둡 보다 **분석 친화적인 스파크**를 주로 사용해 분석하는 추세이다. 스파크가 Pyspark이나 SparkR 같은 다양한 분석 API를 제공하고 있기 때문이다. 참고로 하둡은 Java, Spark는 원래 스칼라 기반이다.

<img src="/img/lecture/spark_frame.png" width="65%">

Source: [Nimisha Sharath Sharma](https://www.linkedin.com/pulse/apache-spark-scala-via-python-nimisha-sharath)

#### 스파크 RDD, DataFrame
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


 - Transfrom: **filter, select, drop, join, etc**
 - Action: **count, collect, show, head, take, etc**

<img src="/img/lecture/spark_le.png" width="70%">

Source: [Birendra Kumar Sahu](http://www.grroups.com/blog/how-spark-deconstructed)

#### 스파크 Modules 
스파크가 최근에 각광을 받게 된 배경에는 스파크가 제공하는 모듈도 영향을 미쳤다. 스파크는 분산처리프레임 위에 **Spark Streaming, SparkSQL, MLlib, GraphX**와 같은 모듈을 제공하여 실시간 수집부터 데이터 추출/전처리, 머신러닝 및 그래프 분석까지 하나의 흐름에 가능하도록 개발되었다. 

 - Spark SQL
    - xxx
 - MLlib (깃헙 코드 추가)
 - Spark Streaming
 - GraphX
 
 
 

