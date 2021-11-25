import re
from rest_framework import serializers
from .models import Genre, Movie


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieSimpleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', ]


class MovieListSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)
    rating_average = serializers.FloatField(read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 
            'title', 
            'overview', 
            'poster_path', 
            'release_date', 

            'is_liked',
            'rating_count',
            'rating_average',
        ]

class MovieSerializer(serializers.ModelSerializer):
    # 모델에 없는 값들 받기
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)
    rating_average = serializers.FloatField(read_only=True)
    is_rated = serializers.BooleanField(read_only=True)
    my_rating = serializers.IntegerField(min_value=1, max_value=5, read_only=True)
    
    credits = serializers.DictField()
    videos = serializers.ListField()
    genres = GenreSerializer(many=True, read_only=True)

    # 영화 등록 시 장르 ID 목록 받기
    # 필드에 선언하면 무조건 fields에 있어야 하므로
    # 등록하지 않을 때는 주석 처리를 통해 필드에서 제외
    # genre_ids = serializers.ListField(write_only=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'tmdb_id',
            'imdb_id',

            'title',
            'overview',
            'poster_path',
            'release_date',
            'adult',

            'likes_count',
            'is_liked',
            'rating_count',
            'rating_average',
            'is_rated',
            'my_rating',

            'genres',
            'credits',
            'videos',
        ]
        read_only_fields = (
            'rating_average', 
            'genres', 
        )
        # 외부 사이트의 vote는 받지 않고, 0으로 초기화

    # save() 메서드 오버라이딩
    def create(self, validated_data):
        # genre ids라는 필드는 없으므로, 따로 뽑아놓음.
        genre_ids = validated_data.pop('genre_ids')

        # 주어진 데이터로 movie 인스턴스 생성
        movie = Movie.objects.create(**validated_data)

        # 영화에 장르 목록을 추가
        for genre in genre_ids:
            movie.genres.add(genre)
        
        # movie 인스턴스 반환
        return movie

    def update(self, movie, validated_data):
        genre_ids = validated_data.pop('genre_ids')
        
        for key, value in validated_data.items():
            setattr(movie, key, value)
            movie.save()
        
        movie.genres.clear()

        for genre in genre_ids:
            movie.genres.add(genre)

        return movie
    