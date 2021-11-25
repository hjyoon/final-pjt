from collections import Counter
from pprint import pprint
from typing import Set

from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from django.db.models.query import Prefetch
from django.http.response import JsonResponse
from django.shortcuts import get_list_or_404
from rest_framework.response import Response

from movies.models import Movie
from movies.serializers import MovieListSerializer


class Recommender:
    """
    주어진 장르와 유사한 최신 영화들을 추천해줍니다.

    Args: 장르 ID를 담은 set, 혹은 영화 ID
    """
    def __init__(self, user=None, movie_pk:int=None, count=None):
        self.user = user
        self.target_movie_pk = int(movie_pk) if movie_pk else None
        self.count = int(count) if count else 10
        
        self.target_genre_set = set()
        self.similar_movies = []
        self.genre_sets_of_similarity = []
        self.recommendation = []

    def get_recommendation(self):
        # 1. 장르 목록 확보 단계 
        if self.target_movie_pk:
            self.obtain_genre_set_from_movie()
        elif self.user:
            self.obtain_genre_set_from_user()
        # pprint(self.target_genre_set)

        # 2. 필터링 단계
        self.obtain_similar_movies()
        # print(self.similar_movies)

        self.filter_similar_movies()
        # pprint(self.genre_sets_of_similarity)

        self.filter_source_movie()


        # 3. 최종 후보 선택
        # a. 장르 유사도만 따져서 선택
        # self.sort_genres_by_similarity()
        # self.choose_by_similarity_first()
        # pprint(self.genre_sets_of_similarity)

        # b. 최신순으로, 장르 유사도는 비례해서 선택
        self.sort_movies_by_release_date()
        self.choose_by_proportion()
        # pprint(self.genre_sets_of_similarity)


        # 4. 시리얼라이저 형태로 반환
        # return self.json_response()
        return self.drf_response()

    def obtain_genre_set_from_movie(self):
        """
        장르 목록 추출
        """
        # 영화로부터 장르 QuerySet 추출
        target_movie = Movie.objects.get(pk=self.target_movie_pk)
        target_genres = target_movie.genres.all()

        # 장르들의 ID를 모음
        target_genre_id_set = set(
            [genre['tmdb_id'] 
            for genre in target_genres.values()]
        )
        self.target_genre_set = target_genre_id_set

    def obtain_genre_set_from_user(self):
        # 현재 유저가 좋아요한 영화 목록
        liked_movies = self.user.liked_movies.all()
        
        # 좋아요한 영화 목록의 장르들 확인
        liked_genres = liked_movies.values('genres')
        liked_genres = [genre['genres'] for genre in liked_genres]

        # 최다 장르 구하기
        counter = Counter(liked_genres)
        most_liked_genres = counter.most_common(4)
        genre_set = set([genre[0] for genre in most_liked_genres])
        self.target_genre_set = genre_set

    def obtain_similar_movies(self):
        """
        영화 전체 목록 순회하며, 
        장르 하나라도 포함된 것 찾기
        (= OR 방식)
        """
        target_genre_set = self.target_genre_set

        self.similar_movies = get_list_or_404(
            Movie.objects
                .prefetch_related(Prefetch('movie_ratings'))
                .annotate(rating_count=Count('movie_ratings'))
                .annotate(rating_average=Avg('movie_ratings__rating'))
                .prefetch_related('genres')
                .filter(genres__tmdb_id__in=target_genre_set)
        )
    
    def filter_similar_movies(self):
        """
        영화 전체 목록 순회하며, 가장 비슷한 장르를 골라내기
        (= AND 방식)
        """
        # 장르 개수만큼 set 리스트 생성
        self.genre_sets_of_similarity = [
            set() for _ in range(len(self.target_genre_set) + 1)
        ]
        
        for movie in self.similar_movies:
            # 현재 영화에 담긴 장르 ID 추출
            current_genre_set = set([genre['tmdb_id'] for genre in movie.genres.values()])
            # 원래 장르 set과 공통 개수 구하기 (by set 교집합)
            similarity = len(self.target_genre_set & current_genre_set)
            # 같은 공통 개수를 가진 set에 추가하기
            self.genre_sets_of_similarity[similarity].add(
                (tuple(current_genre_set), movie)
            )

    def filter_source_movie(self):
        """
        만약 영화가 주어진 경우, 기준 영화는 제외
        """
        if self.target_movie_pk:
            for genre_set in self.genre_sets_of_similarity[-1]:
                # FIXME: str이 아니라 int여야 같은 걸로 취급해서 제외됨.
                if self.target_movie_pk == genre_set[1].id:
                    self.genre_sets_of_similarity[-1].discard(genre_set)
                    return

    def sort_genres_by_similarity(self):
        # 집합들을 리스트로 만들어서 정렬하기
        for idx, genre_sets in enumerate(self.genre_sets_of_similarity[1:], start=1):
            # 이때 장르 개수가 적은 게 먼저 오도록 정렬
            # 그래야 원래 장르 목록과 최대한 비슷하기 때문!
            self.genre_sets_of_similarity[idx] = sorted(
                list(genre_sets), 
                key=lambda genre_info: len(genre_info[0]),
                reverse=True
            )
    
    def sort_movies_by_release_date(self):
        for idx, genre_sets in enumerate(self.genre_sets_of_similarity[1:], start=1):
            # 이때 장르 개수가 적은 게 먼저 오도록 정렬
            # 그래야 원래 장르 목록과 최대한 비슷하기 때문!
            self.genre_sets_of_similarity[idx] = sorted(
                genre_sets, 
                key=lambda genre_info: genre_info[1].release_date,
            )
    
    def choose_by_similarity_first(self):
        idx = len(self.target_genre_set)
        while len(self.recommendation) <= self.count:
            if self.genre_sets_of_similarity[idx]:
                similar_movie = self.genre_sets_of_similarity[idx].pop()
                self.recommendation.append(similar_movie)
            else:
                idx -= 1
                if idx == 0:
                    break
            
        self.recommendation = self.recommendation[:self.count]

    def choose_by_proportion(self):
        """
        장르 공통 개수만큼 뽑기
        => 공통 개수가 많은 쪽에서 더 많이 뽑게 된다.
        """
        idx = len(self.target_genre_set)
        while len(self.recommendation) <= self.count:
            for _ in range(idx):
                if self.genre_sets_of_similarity[idx]:
                    similar_movie = self.genre_sets_of_similarity[idx].pop()
                    self.recommendation.append(similar_movie)
                else:
                    break
            idx -= 1
            if idx == 0:
                idx = len(self.target_genre_set)

        self.recommendation = self.recommendation[:self.count]

    def json_response(self):
        return JsonResponse(self.recommendation, safe=False)

    def drf_response(self):
        recommended_movies = [movie[1] for movie in self.recommendation]
        # pprint(recommended_movies)

        # 유저가 있으면 유저 PK 반영
        user_pk = self.user.pk if self.user else None

        # 각 영화마다 좋아요 개수 추가
        # & 유저가 있을 경우 좋아요 여부 추가
        for movie in recommended_movies:
            movie.is_liked = movie.likers.filter(pk=user_pk).exists()

        serializer = MovieListSerializer(recommended_movies, many=True)
        return Response(serializer.data)