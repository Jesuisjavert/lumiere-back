from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Movie, MovieRankComment
from .serializers import MovieListSerializer, MovieDetailSerializer, MovieRankCommentSerializer
# Create your views here.

@api_view(['GET'])
def index(request):
    movies = Movie.objects.all()[:18]
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, movie_id):
    movie_data = get_object_or_404(Movie, id=movie_id)
    serializer = MovieRankCommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie_data)
        return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_update(request, comment_id):
    try:
        comment_data = MovieRankComment.objects.get(id=comment_id)
    except :
        return Response({'message': '잘못 된 요청입니다.'}, status=status.HTTP_404_NOT_FOUND)
    if request.user == comment_data.user:
        if request.method == 'PUT':
            serializer = MovieRankCommentSerializer(comment_data, data=request.data)
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