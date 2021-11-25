import json
from typing import List
from pathlib import Path
import requests

from . import _env


GET_POPULAR = '/movie/popular'
BASE_URL = 'https://api.themoviedb.org/3'


class TMDB:

    def __init__(self):

        """
        TMDB 인스턴스 생성.\n
        자동으로 환경 변수 파일에서 API key, 언어 옵션, 지역 옵션을 불러옴.
        """

        self.api_key = _env.API_KEY
        self.region = _env.REGION
        self.language = _env.LANGUAGE

    def build_url(self, url, region=False, lang=False, **kwargs):
        request_url = BASE_URL + url
        request_url += f'?api_key={self.api_key}'

        if region:
            request_url += f'&region={self.region}'
        if lang:
            request_url += f'&language={self.language}'

        for key, value in kwargs.items():
            request_url += f'&{key}={value}'

        return request_url

    def fill_image_url(self, movie: dict) -> None:
        
        """
        이미지 크기를 넣어 이미지 URL 채우기
            + 크기는 미리 정해진 옵션만 가능하게
            class 형태로 미리 선언 (small, middle, large)
        """
        
        if 'backdrop_path' in movie:
            backdrop_url_base = 'https://www.themoviedb.org/t/p/w300'
            movie['backdrop_path'] = backdrop_url_base + movie['backdrop_path']

        if 'poster_path' in movie:
            poster_url_base = 'https://www.themoviedb.org/t/p/w780'
            movie['poster_path'] = poster_url_base + movie['poster_path']
        
    def get_genre_dict(self) -> dict:

        """
        TMDB에서 통용되는 영화 장르 ID와 이름을 가져와,\n
        딕셔너리 형태로 반환합니다.
        """

        request_url = self.build_url('/genre/movie/list', lang=True)
        genre_data = requests.get(request_url).json()
        genre_list = genre_data['genres']
        genre_dict = {genre['id']: genre['name'] for genre in genre_list}
        return genre_dict
    
    def save_genre_dict(self) -> None:

        """
        장르 딕셔너리를 JSON 파일로 저장합니다.
        """
        genre_dict = self.get_genre_dict()
        
        # UTF-8 형식으로 저장.
        file_path = Path(__file__).parent / 'genre_dict.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(genre_dict, f, ensure_ascii=False, indent=4)
    
    def load_genre_dict(self) -> dict:

        """
        장르 ID와 이름이 서로 대응되는 딕셔너리를 저장된 파일로부터 불러와 반환합니다.
        
        파일이 없으면, API 요청을 거쳐 저장 한 후에 파일을 불러옵니다.
        """

        while True:
            try:
                file_path = Path(__file__).parent / 'genre_dict.json'
                with open(file_path, 'r', encoding='utf-8') as f:
                    genre_dict = json.load(f)
                break
            
            except FileNotFoundError:
                self.save_genre_dict()
            
        return genre_dict
    
    def load_genre_list(self) -> List[dict]:
        genre_dict = self.load_genre_dict()
        genre_list = [
            {'tmdb_id': key, 'name': value} 
            for key, value in genre_dict.items()
        ]
        return genre_list

    def get_movie_detail(self, movie_id) -> dict:
        request_url = self.build_url(f'/movie/{movie_id}', lang=True)
        movie_detail = requests.get(request_url).json()
        return movie_detail

    def get_movie_videos(self, movie_id) -> List[dict]:
        request_url = self.build_url(f'/movie/{movie_id}/videos', lang=True)
        video_data = requests.get(request_url).json()
        video_list = video_data['results']
        return video_list

    def get_movie_credits(self, movie_id) -> List[dict]:
        request_url = self.build_url(f'/movie/{movie_id}/credits', lang=True)
        credit_data = requests.get(request_url).json()
        
        main_actors = credit_data['cast'][:5]

        crew = credit_data['crew']
        for staff in crew:
            if staff['job'] == 'Director':
                director = staff

        trimmed_credit = {
            'cast': main_actors,
            'director': director
        }
        return trimmed_credit

    
    def get_trimmed_video_list(self, movie_id) -> List[dict]:
        keys = [
            'key',
            'name',
            'site',
            'type'
        ]

        video_list = self.get_movie_videos(movie_id)
        trimmed_video_list = [{key: video[key] for key in keys} for video in video_list]

        for video in trimmed_video_list:
            if video['site'] == 'YouTube':
                video['url'] = f"https://www.youtube.com/watch?v={video['key']}"

        return trimmed_video_list

    def get_popular_movies(self, page_num) -> List[dict]:

        """
        인기 영화 목록 받기
        """

        request_url = self.build_url(GET_POPULAR, region=True, lang=True, page=page_num)
        popular_movie_data = requests.get(request_url).json()
        popular_movie_list = popular_movie_data['results']
        return popular_movie_list

    """
    필요한 기능
    - 저장용: 영화 목록 받고 -> 추출 및 수정해서 -> dict로 반환 (-> 모델에 저장)
    """

    def filter_keys(self, movie: dict) -> dict:

        """
        원하는 key만 가진 딕셔너리 생성하기
        + value 에 의한 필터링은 나중에 추가로 하기 (예: adult 등)        
        """
        
        keys = [
            'adult',
            'genre_ids',
            'id', 
            'overview',
            'poster_path',
            'release_date', 
            'title',
        ]

        # comprehension을 이용해 필터링된 딕셔너리 배열 생성
        trimmed_movie = {key: movie[key] for key in keys}
        
        ### 데이터 가공
        # 이미지 URL 채우기
        # self.fill_image_url(trimmed_movie)

        # id는 'tmdb_id'로 저장
        trimmed_movie['tmdb_id'] = movie['id']
        trimmed_movie.pop('id')
        
        ### 영화 상세 정보 불러와, 데이터 추가
        movie_detail = self.get_movie_detail(movie['id'])
        
        # 'imdb id' 추가
        trimmed_movie['imdb_id'] = movie_detail['imdb_id']
        
        # 영상 리스트 추가
        videos = self.get_trimmed_video_list(movie['id'])
        trimmed_movie['videos'] = videos

        ### 출연진 정보 불러와, 배우랑 감독 추가
        credits = self.get_movie_credits(movie['id'])
        trimmed_movie['credits'] = credits
        
        # 장르 이름 추가... 불필요
        # 이유: GenreSerializer에서 출력 가능
        # genre_dict = self.load_genre_dict()
        # trimmed_movie['genre_names'] = [genre_dict[str(k)] for k in movie['genre_ids']]

        return trimmed_movie

    def get_sample_movies(self) -> List[dict]:

        """
        TMDB로부터 인기 영화 200개(1페이지 당 20개)를 가져온 후, 
        
        데이터 가공해서 반환
        """

        movies = []
        for page in range(1, 11):
            movies.extend(self.get_popular_movies(page))
        filtered_movies = [self.filter_keys(movie) for movie in movies]
        return filtered_movies

    # def get_movie_id(self, title):
    #     """영화 제목을 이용하여 아이디를 추출합니다.

    #     영화 제목을 이용하여 TMDB API 서버에 요청을 보내고 
    #     응답 결과에서 해당 영화의 id 을 반환합니다.

    #     Args:
    #         title: 영화 제목.
        
    #     Returns:
    #         영화 아이디(id)를 반환합니다.
    #         단, 응답 결과가 없을 경우 None을 반환합니다.
    #     """
    #     request_url = self.get_request_url('/search/movie', query=title, region='KR', language='ko')
    #     data = requests.get(request_url).json()
    #     results = data.get('results')
    #     if results:
    #         movie = results[0]
    #         movie_id = movie['id']
    #         return movie_id
    #     else:
    #         return None
