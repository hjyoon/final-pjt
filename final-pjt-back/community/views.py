from django.db.models import Count
from django.db.models.query import Prefetch
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Article, Comment
from .serializers import (
    ArticleSerializer,
    ArticleListSerializer,
    CommentSerializer
)
from utils.paginator import split_into_pages


@api_view(['GET', 'POST'])
def list_article(request):
    """
    글 조회 & 생성 (둘 다 인증 필요)

    - 글 조회 시 query params:
        - page=<page_num>: 원하는 페이지 번호
        - size=<size_num>: 페이지 당 영화 개수
        - (인자가 없는 경우 1 페이지, 20개 반환)

    - 글 생성 시 추가 가능 data:
        - movie: int(pk)
        - movie_title: str
        - rating: int
        - image: str(url)
    """

    if request.method == 'GET':
        articles = get_list_or_404(
            Article.objects
            .prefetch_related(Prefetch('comments'))
            .annotate(comment_count=Count('comments'))
            .order_by('-pk')
        )
        page_object_list = split_into_pages(request, articles)
        serializer = ArticleListSerializer(page_object_list, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def detail_article(request, article_pk):
    """
    개별 글 수정 / 삭제
    - 작성자 본인만 글 수정 / 삭제
    """
    article = get_object_or_404(
        Article.objects
        .prefetch_related(Prefetch('comments'))
        .annotate(comment_count=Count('comments'))
        .filter(pk=article_pk)
    )

    # 작성자가 아닌 경우 수정 불가
    if article.user != request.user:
        return Response({'detail': '작성자가 아닙니다.'}, status.HTTP_403_FORBIDDEN)

    elif request.method == 'PUT':
        # partial: 부분적으로 수정 가능
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        if article.rating_info:
            article.rating_info.delete()
        article.delete()
        return Response({'detail': 'article deleted'}, status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def list_comment(request, article_pk):
    """
    댓글 조회 & 작성 (둘 다 인증 필요)

    - 댓글 조회 시 query params:
        - page=<page_num>: 원하는 페이지 번호
        - size=<size_num>: 페이지 당 영화 개수
        - (인자가 없는 경우 1 페이지, 20개 반환)
    """
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        comments = get_list_or_404(Comment, article=article)
        page_object_list = split_into_pages(request, comments)

        serializer = CommentSerializer(page_object_list, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def detail_comment(request, article_pk, comment_pk):
    """
    댓글 작성자 본인만 댓글 수정 / 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_pk)

    # 작성자가 아닌 경우 수정 불가
    if comment.user != request.user:
        return Response({'detail': '작성자가 아닙니다.'}, status.HTTP_403_FORBIDDEN)

    elif request.method == 'PUT':
        # partial: 부분적으로 수정 가능
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        comment.delete()
        return Response({'detail': 'comment deleted'}, status.HTTP_204_NO_CONTENT)
