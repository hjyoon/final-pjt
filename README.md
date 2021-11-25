# final-pjt

## 팀원 정보 및 업무 분담 내역

- 윤효전 : 프론트엔드 (Vue.js)
- 신인호 : 백엔드 (Django REST)

## 목표 및 필수 서비스 구현 및 실제 구현 정도

### 시스템 구조

![system_structure](https://lab.ssafy.com/se1620236/final-pjt/-/raw/master/System%20Structure.png)



### 관리자 뷰

| 기능                          | 구현 유무 | 비고                     |
| ----------------------------- | --------- | ------------------------ |
| **영화 등록,수정,삭제**       | O         | 장고의 admin 페이지 사용 |
| **유저 관리**                 | O         | 장고의 admin 페이지 사용 |
| **관리자 페이지**             | O         | 장고의 admin 페이지 사용 |
| Vue를 통한 관리자 페이지 제작 |           |                          |

### 인증

| 기능                             | 구현 유무 | 비고 |
| -------------------------------- | --------- | ---- |
| 아이디 찾기                      |           |      |
| 비밀번호 찾기                    |           |      |
| 이메일 인증                      |           |      |
| OAuth2 를 이용한 타서비스로 인증 |           |      |
| 회원 탈퇴                        |           |      |

### 유저

| 기능                     | 구현 유무 | 비고 |
| ------------------------ | --------- | ---- |
| 프로필 사진 등록 및 변경 |           |      |

### 영화 정보

| 기능                                         | 구현 유무 | 비고                      |
| -------------------------------------------- | --------- | ------------------------- |
| **영화 정보 수집**                           | O         | 200 개의 영화 데이터 사용 |
| **로그인 된 유저 영화 평점 등록, 수정 삭제** | O         |                           |
| 영화 리스트 무한 스크롤                      | O         |                           |
| 영화 좋아요 기능                             | O         |                           |
| 영화 즐겨찾기 목록                           |           |                           |
| 영화 공유 기능                               |           |                           |
| 영화 검색 및 필터링 기능                     |           |                           |

### 추천 알고리즘

| 기능              | 구현 유무 | 비고 |
| ----------------- | --------- | ---- |
| **추천 알고리즘** | O         |      |

- 추천 알고리즘은 '좋아요'를 누른 영화들과 **비슷한 장르**를 추천하도록 하였습니다.
  추천은 다음과 같은 방식으로 진행됩니다.

  1. '좋아요'를 누른 영화들의 장르들 중 가장 많이 등장하는 장르들을 기준으로 삼습니다.

  2. 이 장르들을 적어도 하나 포함하는 영화들을 전부 가져옵니다. (inclusive)

  3. 그 중 기준으로 삼은 장르와 최대한 비슷한 장르의 영화들을 선택합니다. (exclusive)

  4. 이 영화들을 최신 영화가 먼저 오도록 정렬하고, 10개를 뽑아 목록을 반환합니다.

     (예전 영화는 봤을 수도 있으므로, 최신 영화가 먼저 오도록 하였습니다.)



### 커뮤니티

| 기능                                      | 구현 유무 | 비고                       |
| ----------------------------------------- | --------- | -------------------------- |
| **영화 정보 관련 대화 기능**              | O         |                            |
| **로그인한 사용자만 글을 조회 및 생성**   | O         |                            |
| **작성자 본인만 글을 수정 및 삭제**       | O         | 평점 등록/수정/삭제도 가능 |
| **댓글 작성 및 작성자 본인 댓글 삭제**    | O         |                            |
| **게시글 및 댓글 생성 및 수정 시각 정보** | O         |                            |
| 댓글의 댓글 기능                          |           |                            |

### 기타

| 기능                                      | 구현 유무 | 비고                                                    |
| ----------------------------------------- | --------- | ------------------------------------------------------- |
| **5개 이상의 URL 및 페이지 구성**         | O         | Home, Login, Registration, Community, Recommendation 등 |
| **HTTP Method 및 상태코드 적절한 사용**   | O         |                                                         |
| **비동기 요청을 통한 사용자 경험 향상**   | O         | fetch, async, await 사용                                |
| 다양한 기기의 해상도를 지원하는 반응형 웹 | △         |                                                         |

## 데이터베이스 모델링 (ERD)

![ERD](https://lab.ssafy.com/se1620236/final-pjt/-/raw/master/final-pjt-back/ERD.png)

## 배포 서버 URL

- 프론트엔드 : https://www.cine-pjt.tk/
- 백엔드 : https://www.movie-vol.ga/

## 기타 (느낀 점)

- 데이터베이스 공부의 필요성
  - 대략 전체 작업 시간의 70% 이상을, modeling과 serializer를 작업하는 데 할애한 것 같습니다.
  - 나머지 시간 중 20% 정도는 애초에 modeling을 이상하게 해서 굳이 어렵게 만드느라 시간을 더 썼던 것 같습니다. 
  - 데이터베이스를 배워야 할 필요성을 절실히 느끼게 해준 기회였다고 생각합니다.
- 문서화 도구의 필요성
  - 이번에 API 문서를 작성하게 되었는데, 이것도 만만찮게 힘들었습니다.
  - 가장 힘들었던 점은, 매번 코드를 수정할 때마다 일일이 수작업을 통해 바꿔줘야 한다는 것이었습니다. 중간에 Swagger라는 문서화 도구를 시험해봤지만, HTTP 응답 부분이 제대로 나오지 않아 다시 수작업으로 복귀했습니다.
  - 2학기 프로젝트를 하기 전에, 일단 가장 제대로 된 문서화 도구를 배워둬야겠습니다.
- 유효성과 보안 문제 신경쓰기
  - 유효성 같은 것도 그동안 생각치 못했던 것이었습니다.
  - 가령 숫자 같은 경우, 항상 최소 범위와 최대 범위를 생각해야 합니다.
    그리고 범위를 벗어나면 어떻게 되는지까지도 정하면 더 좋습니다.
  - 그런데 이게 정확하게 하고자 하면 한도 끝도 없는 개념이라,
    역시 일반적으로 자주 쓰이는 유효성의 개념을 파악해둘 필요가 있겠습니다.
