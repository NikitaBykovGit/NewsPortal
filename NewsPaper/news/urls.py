from django.urls import path
from .views import NewsList, PostsList, PostDetail, PostCreate, PostSearch

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('news/', NewsList.as_view(), name='news')
]