from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from news.views import PostViewSet, NewsViewSet, ArticleViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'articles', ArticleViewSet, basename="artciles")
router.register(r'news', NewsViewSet, basename="news")


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('utils/', include('utils.urls')),
    path('', include('news.urls')),
]
