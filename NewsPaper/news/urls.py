from django.urls import path
from .views import NewsList, ArticlesList, PostsList, PostDetail, ArticleCreate, NewsCreate, PostSearch

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('news/create/', NewsCreate.as_view(), name='post_create'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('news/', NewsList.as_view(), name='news'),
    path('articles/', ArticlesList.as_view(), name='news')
]