from django.urls import path, include
from . import views

urlpatterns = [
    path('scrap/<int:max_num_articles>/', views.scrap, name='scrap'),
    path('article/<int:article_id>/', views.get_article, name='get_article'),
    path('article/<str:keywords>/', views.get_article_with_keys, name='get_article_with_keys'),
]
