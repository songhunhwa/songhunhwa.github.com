---
title: "3회차: 결제 예측 모델링 구축"
layout: post
author: songhunhwa
---

### 목적
 - 결제 행동을 예측하는 모델을 구축하고 평가한다.
 - 실제 분석을 진행하는 상황으로 생각하고 실습을 진행한다.
 
### 목차
 1. 문제 정의 및 가설
 2. 분석 Frame 구성
 3. 데이터 전처리
 4. 데이터 분석
 5. 리포트 작성
 
### 문제 정의 및 가설
여러 번 강조해도 지나침이 없을 정도로, 문제를 명확히 정의/설정하고 목표를 세우는 것은 매우 중요하다. 만약 목표가 틀리다면, 아무리 열심히 수고하더라도 큰 의미가 없기 때문이다.(물론 회사 입장에서 그렇다. 개인 입장에서는 경험치 획득에 도움이 될 수는 있다) 이번에는 마케팅팀에서 업무 요청이 왔다고 가정한다. 마케팅팀이 관심을 두는 것은 회원의 행동 패턴을 근거로, 결제로 전환할 유저를 모델을 통해 예측하는 것이 가능한지 여부이다. 

#### 배경
배경 및 상황에 대해 조금더 자세히 살펴보자. 마케팅팀은 주로 예산을 집행하고 이에 따른 결과(성과)를 통해 예산을 효율화하는 것이 관심을 두고 있다. 이를 위해 흔히 알려진 전략이 STP이다. 즉 유저/소비자를 세분화해 그룹으로 나누고, 각 그룹에 맞는 개인화 메시지를 전달하거나 그룹의 우선순위에 따라 예산 및 접근 방식에 차등을 두는 방식을 주로 이용한다. 이번 사례에서는 결제자의 수를 증가시키기 위한 비즈니스 전략을 달성하기 위해 마케팅팀으로부터 결제자 예측 모델링 구축 관련한 업무 요청이 왔다고 가정하고 진행한다.
 
 - 결제자수의 증가에 대한 비즈니스 요구 발생 (마케팅팀 KPI)
 - 유저의 행동을 기반으로, 결제 가능성이 높은 유저를 선별하여 해당 유저를 위주로 타깃팅 (광고, 프로모션 등)
 - 데이터 분석가 뿐만 아니라, 여러 팀의 협업이 필요한 상황
  
#### 목적
이번 사례의 경우 아래와 같이 데이터 분석가의 목적을 설정할 수 있다. 단, 지금 사례와 같이 여러 팀이 협업해서 프로젝트를 진행하는 경우라면 전체 프로젝트의 목적과 각 팀 혹은 파트 별로의 목적을 충분한 논의를 통해 설정하는 것이 필요하다. 

 - 결제자로 전환할 가능성이 높은 유저를 판별하는 모델 구축
 - 예측 모델의 성능을 측정할 수 있는 지표를 정의

<img src="/img/lecture/predmodel.png" width="65%">

#### 가설
이번 사례의 경우 가설을 설정하기 위해 도메인 지식이 많이 요구된다. 도메인 지식과 전문가의 조언 등을 통해 결제와 관련 있는 행동 변수를 사전에 이해하고 리스트업하는 것이 유용하다. 만약 이러한 도움을 받기 어려운 상황이라면, 분석가의 상상력과 직감을 이용해 주요 변수들을 생각해놓고 탐색적 데이터 분석을 통해 Feature Selection을 하는 것이 필요하다. 예를 들어 아래와 
- 가설 1: Open, Edit/Save, Export와 같은 문서 이용행동 관련 변수가 모델 구축에 유의미한 변수일 것
- 가설 2: 문서 사용 트래픽 및 일주일 간 방문일수 역시 결제 행동와 관련 있는 예측 변수일 것

#### Expected Output
- 타깃팅 유저 정보 테이블 (RDB, 일별 배치)
	- Schema: 날짜, 타깃팅 대상 유저의 아이디, 결제 확률, 결제 예상 여부 (결제 확률 50% 이상일 경우 True, 이하일 경우 False)
- 타깃팅 결과 테이블 (RDB, 일별 배치)
	- Schema: 날짜, 타깃 유저 아이디, 타깃 액티비티, 결제 여부(기존 3일내) 
- 결제 정보 테이블 (기존 Hadoop 저장 테이블)
	- Schema: 날짜, 전체 결제 유저 아이디, 결제일
- 모델 구축 과정 문서(수식) 및 코드
- 모델 성과 측정 대시보드/리포트 (Recall, Precision, AUC, F1-score)

### 분석 Frame
일반적인 모델링 구축을 위한 프로세스를 먼저 살펴보자.

<img src="/img/lecture/class_process.png" width="80%">

Source: [Algoline](http://algolytics.com/tutorial-how-to-determine-the-quality-and-correctness-of-classification-models-part-1-introduction/)

이번 프로젝트 역시 일반적이 프로세스와 거의 유사하게 진행될 것이다. 리포트 및 공유 문서에 위와 같은 프레임 이미지를 협업자에게 보여준다면 모델링 프로세스에 대한 이해가 높아질 것으로 기대할 수 있다. 위 이미지를 참고하여 이번 프로젝트의 프레임을 구성해보자.

- 데이터 수집
	- 결제 바로 전, 유저의 행동 패턴을 기술할 수 있는 로그 항목을 수집 (문서 오픈, 편집 등)
- 데이터 추출
	- Extraction, Preprocessing (SQL 필터, 조인 등)
- 데이터 전처리
	- Feature Engineering (분포 변환, PCA, 결측치 및 이상치 처리 등)
- 모델 구축
	- Classification Models (Logistic Regression, Random Forest, etc)
	- Cross Validation, Grid Search, Pipeline
- 모델 평가
	- Precision, Recall, F1-score

#### Logic Tree
지난 시간에 배운 로직 트리를 이용해 전체적인 흐름을 구성하도록 하자. 모델을 구축하고 평가하는 분석가의 role은 일반적으로 큰 프로젝트 안에서 하나의 부분(part)를 맡게 된다. 비즈니스 환경에서는 단순히 모델을 구축하는 것이 목적이 되기 보다, 별도의 목표를 달성하기 위한 하나의 수단에 지나지 않는 경우가 많다. 따라서 전체 프로젝트(숲)을 보고 상황에 맞게 도구(나무)를 활용하려는 노력이 필요하다. 로직트리를 구성할 때는 전체적인 프로젝트를 고려하면서 짜는 것이 유용할 수 있다.

#### [실습. 결제 예측 모델링 Logic Tree 설계](https://github.com/songhunhwa/songhunhwa.github.com/tree/master/tutorial/tutorial_03)

<img src="/img/lecture/logic_tree_t3.png" width="80%">

#### 추가 고려사항
대부분의 분석 프로젝트도 마찬가지지만, 예측 모델링을 활용하는 프로젝트의 경우 특히 타팀과 팀원간 많은 협업이 요구된다. 분석가가 관여하는 부분은 데이터를 입수해 모델을 구축하고 평가 과정을 통해 최종적인 모델을 만드는 과정이며, 분석가가 만든 프로토타입 코드를 엔지니이와 개발자가 제품에 녹이는 과정도 요구된다. 또 기획 및 운영 등 여러 팀이 관여하게 되므로 전체적인 PM의 역할이 특히 더 중요하다고 할 수 있다.

- 전체적인 그리고 세부적인 일정이 어떻게 되는가? 모델링과 관련된 일정을 맞출 수 있는가?
- 각 팀 및 담당자의 역할은 정확히 무엇인가?
- 엔지니어 및 개발 담당은 누구이며, 어떠한 사항이 논의되어야 하는가? 분석 및 개발 언어는? 제품 내 모델 및 데이터 처리 방식은?
- 정확한 목적은 무엇이며 목표 달성 수준은 어떻게 정의할 것인가?
- 필요한 데이터가 무엇인가? 확보가 가능한가?

### [데이터 전처리](http://www.cs.ccsu.edu/~markov/ccsu_courses/datamining-3.html)
모든 데이터 분석 프로젝트에서 데이터 전처리는 반드시 거쳐야 하는 과정이다. 대부분의 데이터 분석가가 좋아하지 않는 과정이지만, 분석 결과/인사이트와 모델 성능에 직접적인 영향을 미치는 과정이기 때문에 중요하게 다루어지는 과정이다. 한 설문조사에 의하면, 분석가의 80% 시간을 데이터 수집 및 전처리에 사용한다고 하니, 얼마나 중요한 과정인지 짐작할 수 있다. 물론 지루하고 반복 작업의 연속이기 때문에 시간이 많이 들어가는 측면도 있을 것이다.

<img src="/img/lecture/time_consum.png" width="80%">

Source: [Forbes](https://www.forbes.com/sites/gilpress/2016/03/23/data-preparation-most-time-consuming-least-enjoyable-data-science-task-survey-says/#7a9598f66f63)

지난 시간에 간단히 언급한 대로, 실무에 사용되는 데이터셋은 바로 분석이 불가능할 정도로 지저분(messy)하다. 분석이 가능한 상태로 만들기 위해 아래와 같은 전처리 방식이 자주 사용된다. 모든 강의에 걸쳐서 전처리 단계는 중요하게 그리고 반복적으로 다루어질 예정이다. 

#### 결측치 처리
결측치 처리는 1) 결측치 사례 제거 2) 수치형의 경우 평균이나 중앙치로 대체(imputation)하거나 범주형인 경우 mode 값으로 대체 3) 간단한 예측 모델로 대체하는 방식이 일반적으로 이용된다. 가장 쉬운 방법은 Null이 포함 행 혹은 일부 행을 제거하는 것이다. 수집된 사례(observation)이 많다면 이 방법을 사용하는 것이 가능하다. 만약 샘플수가 충분하지 않을 경우, Pandas의 fillna() 명령어로 Null 값을 채우는 것이 가능하다. 연속형인 경우 Mean이나 Median을 이용하고 명목형인 경우 Mode(최빈치)나 예측 모형을 통해 Null 값을 대체할 수 있다.
   
데이터셋을 읽었다면, Missing Value 파악을 위해 df.info() 가장 처음에 이용하는 것을 추천한다. 만약 np.nan으로 적절히 missing value로 불러왔다면 info() 이용 가능하다. 만약 '', ' ' 이런식의 공백이나 다른 방식으로 처리되어 있다면, 모두 repalce 처리해줘야 한다. info()를 실행했을 때, 누가봐도 float or int 인데 object(string)으로 되어 있다면 이런 사레가 포함될 가능성이 높다.   

#### 결측치를 처리할 때 고려할 점
결측치를 처리할 경우에도 도메인 지식은 유용하게 사용된다. 인적, 기계적 원인임이 판명되면, 협업자와 지속적으로 노력해 결측치를 사전에 발생하지 않도록 조치하는 것이 좋다. 수치형인 경우 의미상으로 0으로 메꾸는 것이 맞는지 아니면 평균이나 중앙치가 맞는지 등은 데이터에 대한 배경지식이 있는 경우 보다 적절한 의사결정을 할 수 있다. NA 와 Null 차이는 R에서만 구분되는 개념으로 파이썬에서는 numpy의 NaN만 이용한다.

- NA: Not Available (does not exist, missing)
- Null: empty(null) object
- NaN: Not a Number (python)
- 숫자 0과 NaN 같은 결측치는 완전히 다른 개념이니 유의해야 한다

#### 이상치 처리
일반적으로 1) 표준점수로 변환 후 -3 이하 및 +3 제거 2) IQR 방식 3) 도메인 지식 이용하거나 Binning 처리하는 방식이 이용된다. 표준점수 이용할 경우 평균이 0, 표준편차가 1인 분포로 변환한후 +3 이상이거나 -3 이하인 경우 극단치로 처리한다.

<img src="/img/lecture/zscore_od.png" width="40%">

IQR 방식은 75% percentile * 1.5 이상이거나 25 percentile* 1.5 이하인 경우 극단치로 처리하는 방식이다. 이해하기 쉽고 적용하기 쉬운 편이지만, 경우에 따라 너무 많은 사례들이 극단치로 고려되는 경우가 있다. 

<img src="/img/lecture/IQR.png">

Source: [Wikipedia](https://en.wikipedia.org/wiki/Interquartile_range)

#### [실습. 데이터 전처리](https://github.com/songhunhwa/songhunhwa.github.com/tree/master/tutorial/tutorial_03)

#### 데이터 변환
대부분의 모델은 변수가 특정 분포를 따른다는 가정을 기반으로 한다. 예를 들어 선형 모델의 경우, 설명 및 종속변수 모두가 정규분포와 유사할 경우 성능이 높아지는 것으로 알려져 있다. 자주 쓰이는 방법은 Log, Exp, Sqrt 등 함수를 이용해 데이터 분포를 변환하는 것이다. 

```python
import math
from sklearn import preprocessing

df['X_log'] = preprocessing.scale(np.log(df['X']+1)) # 로그
df['X_sqrt'] = preprocessing.scale(np.sqrt(df['X']+1)) # 제곱근
```

위 방법 외에도 분포의 특성에 따라 제곱, 자연로그, 지수 등 다양한 함수가 사용될 수 있다. 가이드는 아래와 같다.

- left_distribution: X^3
- mild_left: X^2
- mild_right: sqrt(X)
- right: ln(X)
- servere right: 1/X

데이터의 스케일(측정단위)이 다를 경우 특히 거리를 기반으로 분류하는 모델(KNN 등)에 부정적인 영향을 미치므로, 스케일링을 통해 단위를 일정하게 맞추는 작업을 진행해야 한다. 아래 방식이 주로 스케일링을 위해 쓰이는 방법이다.

- Scaling: 평균이 0, 분산이 1인 분포로 변환
- MinMax Scaling: 특정 범위 (예, 0~1)로 모든 데이터를 변환
- Box-Cox: 여러 k 값중 가장 작은 SSE 선택
- Robust_scale: median, interquartile range 사용(outlier 영향 최소화)

```python
from scipy.stats import boxcox

df['X_scale'] = preprocessing.scale(df['X']) 
df['X_minmax_scale'] = preprocessing.MinMaxScaler(df['X']
df['X_boxcox'] = preprocessing.scale(boxcox(df['X']+1)[0])
df['X_robust_scale'] = preprocessing.robust_scale(df['X'])
```

대부분의 통계 분석 방법이 정규성 가정을 기반으로 한다. 따라서 완벽하지 않더라도 최대한 정규분포로 변환하는 노력이 필요하다. Normalization은 스케일링과 다르게, 각 요소간 상대적 거리를 유지하면서 다른 측정 값으로 변환시 사용한다.

#### [실습. 데이터 전처리](https://github.com/songhunhwa/songhunhwa.github.com/tree/master/tutorial/tutorial_03)

### 모델 구축
데이터 전처리가 끝났다면, 아래와 같은 프로세스로 모델을 구축한다. 모델링 단계에 들어왔어도 데이터 전처리는 끝난 것은 아니다. 모델의 성능은 알고리즘의 차이 보다 전처리를 어떻게 했는지에 따라 더 많이 영향을 받는 것으로 알려져 있다. 따라서 모델의 성능을 측정해보고 결과가 만족스럽지 않다면, (여러 알고리즘을 사용해보는 것과 더불어) 전처리 단계를 다시 진행해야 할 수도 있다. 또 전처리를 잘하기 위해선 EDA/시각화 과정을 반복해서 진행할 필요가 있다.

<img src="/img/lecture/modeling_process.png" width="60%">

#### 모델을 구축하면서 고려할 점
- 목적과 데이터 특성에 맞는 모델은 무엇인가?
- 일반화 가능성은 어떠한가? (overfitting, underfitting의 가능성은?)
- 성능 측정의 지표는? 성능을 높이기 위해 어떻게 Feature Engineering 을 진행할 것인가?
- 제품 혹은 시스템에 모델을 적용할시 계산량이나 언어 특성에 관해 고려할 부분은 무엇인가?
- 모델/파라메터 업데이트 주기 및 방식은 어떻게 협의할 것인가?

#### Cross Validation
구축된 모델의 일반화 가능성, 즉 overfitting, underfitting을 다루는 문제는 매우 중요하다. 이를 효과적으로 다룰 수 있는 방법이 Cross Vaildation이다. Cross Validation은 아래와 같은 순서로 진행된다.
- 전체 데이터셋을 3파트로 랜덤하게 분류
	- 50%: train
	- 20%: validation (for grid search)
	- 30% test (to be used just once at the last moment)

```python
from sklearn.cross_validation import train_test_split

X_trainval, X_test, y_trainval, y_test = train_test_split(X, y, random_state=23)
X_train, X_val, y_train, y_val = train_test_split(X_trainval, y_trainval, random_state=11)
```

- Grid Search를 통해 최적의 파라메터 도출
	- K-fold
	- Stratified k-fold
	- LOOCV

```python
from sklearn.model_selection import GridSearchCV

param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100],
              'penalty': ['l1', 'l2']}
grid_search = GridSearchCV(LogisticRegression(), param_grid, cv=5)	      

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=23)

grid_search.fit(X_train, y_train)
grid_search.score(X_test, y_test)
```

<img src="/img/lecture/kfold.png" width="60%">


#### Evaluation
최적의
