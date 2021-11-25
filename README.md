# final-pjt

## 팀원 정보 및 업무 분담 내역

- 윤효전 : 프론트엔드
- 신인호 : 백엔드

## 목표 및 필수 서비스 구현 및 실제 구현 정도

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

| 기능              | 구현 유무 | 비고                |
| ----------------- | --------- | ------------------- |
| **추천 알고리즘** | O         | 평점 등록 기반 추천 |

### 커뮤니티

| 기능                                      | 구현 유무 | 비고 |
| ----------------------------------------- | --------- | ---- |
| **영화 정보 관련 대화 기능**              | O         |      |
| **로그인한 사용자만 글을 조회 및 생성**   | O         |      |
| **작성자 본인만 글을 수정 및 삭제**       | O         |      |
| **댓글 작성 및 작성자 본인 댓글 삭제**    | O         |      |
| **게시글 및 댓글 생성 및 수정 시각 정보** | O         |      |
| 댓글의 댓글 기능                          |           |      |

### 기타

| 기능                                      | 구현 유무 | 비고                                                    |
| ----------------------------------------- | --------- | ------------------------------------------------------- |
| **5개 이상의 URL 및 페이지 구성**         | O         | Home, Login, Registration, Community, Recommendation 등 |
| **HTTP Method 및 상태코드 적절한 사용**   | O         |                                                         |
| **비동기 요청을 통한 사용자 경험 향상**   | O         | fetch, async, await 사용                                |
| 다양한 기기의 해상도를 지원하는 반응형 웹 | △         |                                                         |

## 데이터베이스 모델링 (ERD)

## 배포 서버 URL

- 프론트엔드 : https://www.cine-pjt.tk/
- 백엔드 : https://www.movie-vol.ga/

## 기타 (느낀 점)
