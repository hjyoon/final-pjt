from rest_framework import serializers

from accounts.serializers import UserSerializer
from movies.models import Movie, Rating
from .models import Article, Comment


class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'user',
            'content',
            'created_at',
            'updated_at',
            'comment_count',
            'movie',
            'movie_title',
            'rating',
            'rating_info',
            'image',
        ]
        read_only_fields = ['rating', 'rating_info', ]


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField(
        min_value=1, 
        max_value=5, 
        required=False
    )

    class Meta:
        model = Article
        fields = [
            'id',
            'user',
            'content',
            'created_at',
            'updated_at',
            'comment_count',
            'movie',
            'movie_title',
            'rating',
            'rating_info',
            'image',
        ]
        read_only_fields = ['rating_info', ]

    def get_article(self, data, instance=None):
        if instance:
            user = instance.user
        else:
            user = data.get('user')
        return Article.objects.filter(
            movie=data.get('movie').id,
            user=user
        )

    def get_rating_info(self, data):
        return Rating.objects.filter(
            movie=data.get('movie'),
            user=data.get('user')
        )

    def validate(self, data):
        """
        평점이 있는 경우, 반드시 대상이 되는 영화가 있어야 함.

        * 영화 ID는 자체적으로 범위 벗어나면 오류남.
        """
        if data.get('rating'):
            if data.get('movie') or data.get('movie_title'):
                pass
            else:
                detail = 'movie (or movie_title) is needed if rating exists.'
                raise serializers.ValidationError(detail)
        
        return data
    
    def create(self, data):
        # 기존에 평점을 매겼는지 체크
        # NOTE: update와 차이가 있으므로, validate에 못 넣음.
        if data.get('rating') and data.get('movie'):
            # 해당 유저가 해당 영화에 대해 이미 평점을 매긴 경우
            rating_info = self.get_rating_info(data)
            if rating_info.exists():
                # 오류 메시지와 함께 해당 글 번호 반환
                article = self.get_article(data)
                detail = {
                    'detail': 'user has already rated the movie.',
                    'id': article.get().id
                }
                raise serializers.ValidationError(detail)

        # 평점 매긴 적이 없으면 게시글 생성
        article = super().create(data)

        # 영화가 DB에 있을 때
        if data.get('movie'): 
            # 영화 제목도 DB에 있는 걸로 반영
            article.movie_title = article.movie.title

            # 영화 + 평점까지 있던 경우, 평점도 기록
            if article.rating:
                rating_info = Rating(
                    user=article.user,
                    movie=article.movie,
                    rating=article.rating,
                )
                rating_info.save()
                article.rating_info = rating_info
        
        article.save()
        return article

    def update(self, instance, data):
        """
        평점을 바꾸거나
        평점만 지우거나
        내용 수정 가능
        """
        # 평점이 있는지 체크
        if data.get('rating') and data.get('movie'):
            # 해당 유저가 해당 영화에 대해 이미 평점을 매긴 경우
            rating_info = self.get_rating_info(data)
            if rating_info.exists():
                # 오류 메시지와 함께 해당 글 번호 반환
                another = rating_info.article
                # 이 게시글이랑 ID 다르면 => 중복
                if another.id != instance.id:
                    context = {
                        'detail': 'user has already rated the movie.',
                        'id': another.id,
                    }
                    raise serializers.ValidationError(context)

        article = super().update(instance, data)

        # 게시글에 등록한 영화가 DB에 있을 때
        if data.get('movie'):
            # 영화 제목도 DB에 있는 걸로 반영
            article.movie_title = article.movie.title
        
            if data.get('rating'):
                # 레이팅 정보가 있는지 검사
                if not article.rating_info:
                    # 없었으면 새로 생성
                    rating_info = Rating(
                        user=article.user,
                        movie=article.movie,
                        rating=article.rating,
                    )
                    rating_info.save()
                    article.rating_info = rating_info
                else:
                    # 있었으면 내용만 교체
                    rating_info = article.rating_info
                    # 영화가 다르면 영화만 교체
                    if rating_info.movie != article.movie:
                        rating_info.movie = article.movie
                    rating_info.rating = article.rating
                    rating_info.save()

        # 평점 복구
        if data.get('rating'):
            article.rating = data.get('rating')

        article.save()
        return article


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 
            'article', 
            'user', 
            'content',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['article', ]
