from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Movie, MovieRankComment

class MovieRankCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = MovieRankComment
        # fields = '__all__'
        exclude = ['movie']

class MovieListSerializer(serializers.ModelSerializer):
    comments = MovieRankCommentSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'

class MovieDetailSerializer(serializers.ModelSerializer):
    comments = MovieRankCommentSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'