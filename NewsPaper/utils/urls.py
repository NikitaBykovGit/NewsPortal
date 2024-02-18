from django.urls import path

from .views import TimeZone

urlpatterns = [
    path('timezone/', TimeZone.as_view(), name='set_timezone'),
    ]
