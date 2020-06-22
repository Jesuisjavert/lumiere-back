from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Article, ArticleComment
from .serializers import ArticleCommentSerializer, ArticleSerializer, ArticleDetailSerializer, ArticleListSerializer
# Create your views here.

@api_view(['GET'])
def index(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)

@api_view(['GET'])
def detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    serializer = ArticleDetailSerializer(article)
    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update(request, article_id):
    article_data = get_object_or_404(Article, id=article_id)
    if request.user == article_data.user:
        if request.method == 'PUT':
            serializer = ArticleSerializer(article_data, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'message': '유효성이 잘못 된거 같은데?'}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'DELETE':
            article_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': '유저인증이 잘못 된거 같은데?'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, article_id):
    article_data = get_object_or_404(Article, id=article_id)
    serializer = ArticleCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, article=article_data)
        return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_update(request, comment_id):
    comment_data = ArticleComment.objects.get(id=comment_id)
    if request.user == comment_data.user:
        if request.method == 'PUT':
            serializer = ArticleCommentSerializer(comment_data, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'message': '유효성 검사에서 걸린거같은데?'}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'DELETE':
            comment_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': '유저인증이 잘못 된거 같은데?'}, status=status.HTTP_404_NOT_FOUND)