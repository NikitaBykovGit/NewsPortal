from django.urls import path
from .views import (NewsList, PostsList, PostDetail, PostCreate, PostSearch, PostUpdate,
                    PostDelete, subscriptions, ProfileDetail, Addlike, AddDislike, TimeZone)

urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('timezone', TimeZone.as_view(), name='set_timezone'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('profile/<int:pk>', ProfileDetail.as_view(), name='profile'),
    path('<str:type>/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('<str:type>/create/', PostCreate.as_view(), name='post_create'),
    path('<str:type>/<int:pk>/update', PostUpdate.as_view(), name='post_update'),
    path('<str:type>/<int:pk>/like', Addlike.as_view(), name='like'),
    path('<str:type>/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),
    path('<str:type>/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<str:type>/', NewsList.as_view(), name='news')
]
