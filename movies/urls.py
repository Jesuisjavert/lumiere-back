from django.urls import path, include
from . import views


app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('<int:movie_id>/comment_create', views.comment_create, name='comment_create'),
    path('comment_update/<int:comment_id>', views.comment_update, name='comment_update')
]