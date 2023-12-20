# PROJECT: 서울산책
## 소개

서울특별시 2030 세대의 여가활동 현황은 실내 활동 위주의 여가활동이 절반 이상이지만 희망 여가 활동은 야외 활동이 우세하다는 설문 결과가 있습니다.
또한 움직이지 않고 실내에서 SNS만 하는 생활 패턴으로 인해, 우울증 비율이 급격하게 높아진 것을 알 수 있습니다.
즉, 건강한 생활 습관을 가질 수 있도록 도움이 필요하며 야외 활동을 자주 할 수 있도록, 취미를 만들 수 있도록 하는 것이 중요하다고 느꼈습니다.

따라서 서울의 다양한 실외, 실내활동을 한눈에 보여주는 사이트를 개발하였습니다.


### 2030 세대들의 니즈
- 실외활동 희망
- 재정상태로 인한 스트레스
- 우울감 해소


### 프로젝트의 방향성
- 값싸며 재미있는 실외활동을 한 눈에 보이도록 소개하는 프로젝트를 만들어보자!
- 개인 취향에 따라 추천 장소가 다르도록 설정하는 프로젝트를 만들어보자!



### 팀 구성
![](https://github.com/seoyun-dev/MZplace/raw/main/members.png)
- FE : [Github](https://github.com/JJongsKim/Seoul-Walk)
- BE : [Github](https://github.com/seoyun-dev/MZplace)

### 개발 기간
- 개발 기간 : 2023-10-15 ~ 2023-12-06
- 협업 툴 : Github, Notion


## 김가연(ML)의 기여

### 사용한 공공 데이터 목록
 - [서울시 문화공간 정보](https://data.seoul.go.kr/dataList/OA-15487/S/1/datasetView.do)
 - [서울시 문화행사 정보](https://data.seoul.go.kr/dataList/OA-15486/S/1/datasetView.do)
 - [서울시 생활체육 프로그램](https://data.seoul.go.kr/dataList/OA-21780/S/1/datasetView.do)
 - [서울시 도시갤러리 목록](https://data.seoul.go.kr/dataList/OA-21241/S/1/datasetView.do)
 - [서울시 책방 현황](https://data.seoul.go.kr/dataList/OA-21062/S/1/datasetView.do) 
 - [서울 미래유산 체험코스](https://data.seoul.go.kr/dataList/OA-15447/S/1/datasetView.do)
 

### 데이터 전처리 
- 자치구 결측치 : 정규식으로 주소에서 '-구' 단어 추출
- 위도, 경도 결측치 : 지오코딩
- 이미지 결측치 : 동적 크롤링

### 최종 데이터
공공 데이터 파일을 전처리하여 총 6개의 테이블을 생성
 - places.csv (총 1900개 장소)
 - [categories.csv](https://github.com/maryrichard1022/capstone2/files/13724365/categories.csv) (카테고리별 탐색)
 - filters.csv, filters_places.csv (맞춤 필터 기능)
 - courses.csv, courses_places.csv (미래유산코스)


### 추천 알고리즘 개발

- 찜 기반 장소 추천 (UBCF + IBCF 알고리즘)
  사용자 기반 협업 필터링, 아이템 기반 협업 필터링을 이용하여 사용자가 찜한 장소를 기반으로 다른 장소를 추천하는 알고리즘을 개발 
 

## 사이트 시연 영상
- [서울산책 유튜브 시연영상](https://www.youtube.com/watch?v=bkNFukoFNGQ)
