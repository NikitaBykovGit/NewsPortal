from django.urls import path
from .views import (NewsList, ArticlesList, PostsList, PostDetail, ArticleCreate, NewsCreate, PostSearch, PostUpdate,
                    PostDelete)

urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('articles/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/update', PostUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/<int:pk>/update', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('news/create/', NewsCreate.as_view(), name='post_create'),
    path('news/', NewsList.as_view(), name='news'),
    path('articles/', ArticlesList.as_view(), name='news')
]