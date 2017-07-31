---
title: "분석 준비"
layout: post
author: songhunhwa
---

## Preparation
 
### 1.1 필수 프로그램/라이브러리 설치
 - Anaconda 2.7 버전 (Python, Jupyter 등 필수 프로그램을 패키지로 설치 가능) [Download Anaconda](https://www.continuum.io/downloads)
 - 필수 라이브러리 목록: **Numpy, Pandas, Matplotlib, Seabron, Scipy, Statsmodel, Scikit-learn**

 - 데이터셋 입력, 데이터셋 탐색 (행열의 개수, 변수의 형태 등 파악) → **Numpy, Pandas**
 - 데이터셋 변환 (변수 형태 변환, 파생변수 생성, 변수 삭제, 이상치 제거, 필터, 정렬 등) → **Pandas, Numpy, Scikit-learn**
 - 기술 통계 분석 (평균, 표준편차, 빈도수, 비율 확인, 상관분석 등) → **Pandas, Numpy**
 - 추론 통계 분석 (가설 검증, 분포 추정, 신뢰구간 확인 등) → **SciPy, StatsModel**
 - 기계 학습 (회귀분석, 의사결정나무, 연관성 분석 등) → **Scikit-learn, StatsModels**
 - 시각화 → **Matplotlib, Seaborn**
 - 코드 편집기 → **Jupyter Notebook**

### 1.1 라이브러리 상세 소개

- 이번 포스트에서는 데이터 분석을 위해 사용되는 필수적인 파이썬 모듈(패키지)에 대해 간단히 살펴보고자 합니다. 데이터 분석의 과정을 단계로 별로 나누면 아래와 같고, 단계별로 주로 쓰이는 모듈을 옆에 기술하였습니다. 
  (아래는 절대적인 사항은 아니며, 분석 상황이나 분석가에 따라 많이 달라지는 부분이니 참고만 해주시길 바라겠습니다)


#### Pandas
 - 데이터 입출력 단계부터 기술통계 분석 단계까지 필요한 대부분의 함수와 기능을 담고 있는 모듈입니다. 
 - 아마도 파이썬이 분석툴로 인정받고 많은 분석가들이 사용하는 데 지대한 공헌을 한 모듈이 Pandas가 아닐까 싶습니다. 모든 분석 업무가 가설 검증을 하거나 기계학습을 위해 진행되는 것은 아닙니다. 
   간단히 평균을 도출하거나 빈도 수를 세거나 전환율을 구하는 등 기술 통계 분석에서 업무가 끝나는 경우도 많이 있습니다. 
   입력부터 기술 통계 분석 단계까지, Pandas는 데이터 분석가에게 매우 훌륭한 기능을 제공하는 모듈임은 틀림 없습니다.
 - Reference: http://pandas.pydata.org/pandas-docs/version/0.15.0/index.html#

#### Numpy
 - Numpy는 주로 산술 연산을 위해 이용되는 모듈로, 주로 산술 연산을 위해 Pandas와 병행되는 모듈입니다. 
 - 저 같은 경우 대부분의 연산은 Pandas에서 대부분 가능하기 때문에 Numpy는 변수 타입을 바꾸거나, N/A 값을 입력/처리하는 정도로 이용하고 있습니다.
 - 또 소수점 아래를 무조건 버리거나 무조건 올림하는 경우에도 Numpy의 floor와 celing 함수를 사용합니다. 
   Python으로 산술 연산할 때 Pandas와 Numpy 혼용하다보니 실제 이 함수가 Pandas에 속하는지 Numpy에 속하는지 인지하지 않고 분석 진행하는 경우도 있는데요. 
 - 원하는 결과가 빠르고 정확하게 나오면 되니까요. 아무튼 Numpy는 Pandas와 병행해서 써야 하는 필수 모듈이라고 할 수 있겠습니다.
 - Reference: http://www.numpy.org/

#### Matplotlib & Seaborn
 - 데이터에 대한 분포를 확인하거나 분석 결과를 시각화하는 작업은 필수 과정이라고 할 수 있습니다. 분석 결과를 효과적으로 전달하기 위해서는 단순히 숫자를 나열하는 것보다 시각화하는 것이 훨씬 직관적이기 때문인데요. 시각화를 위해 가장 많이 되는 이용되는 모듈이 바로 Matplotlib 입니다. 
 - Matplotlib가 기본적인 시각화를 대부분 지원하나, 이보다 더욱 고급스러운 시각화 기능을 제공하는 모듈이 Seaborn 입니다. Seaborn이 지원하는 시각화 종류가 훨씬 다양하고 상세한 옵션을 조정할 수 있기 때문에, Matplotlib와 병행해서 쓰이고 있습니다.
 - Matplotlib Reference: http://pandas.pydata.org/pandas-docs/stable/visualization.html
 - Seaborn Reference: https://stanford.edu/~mwaskom/software/seaborn/index.html

#### Scikit-learn
 - 분류, 회귀분석, 클러스터링 등 기계 학습을 위해 주로 이용되는 모듈입니다. 기계학습 뿐아니라, Scaling, 표준화(Normalization), 변수 선택(Feature Extraction) 등 전처리 작업과 PCA, 요인분석 등 차원축소 기능까지 지원합니다. 
   R의 풍부하고 다양한 라이브러리에 비해 기능은 부족하지만, 기본적이고 중요한 대부분의 기능을 지원하고 있어, 데이터 분석(특히 기계학습)에 필수적인 모듈이라고 할 수 있습니다.
 - Reference: http://scikit-learn.org/stable/index.html

#### SciPy, StatsModels
 - 주로 T-test 및 F-test 등 추론 통계 분석을 위해 이용되는 모듈이며, StatsModels는 회귀분석을 할 때 주로 사용되는 모듈입니다. 
 - SciPy Reference: http://docs.scipy.org/doc/scipy/reference/index.html
 - StatsModels Reference: http://www.statsmodels.org/dev/index.html


### 1.2 How to use Jupyter Notebook
 - 목적: Jupyter Notebook에 대한 주요 기능을 파악하고 실습한다
 - 실습과제: H 키를 눌러 Keyborad shortcut을 확인한다.
 - 실습과제: 자주 사용하는 Shortcut을 외운다 (Shift + Enter등)


