from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('choose/', views.choose, name='choose'),
    path('<int:movie_id>/', views.watch, name='watch'),
    path('filter/', views.filter, name='filter'),
    path('random/', views.random_movie, name='random'),
]
