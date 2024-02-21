from django.contrib.auth.models import User

from .models import Post, Author
from rest_framework import serializers


class PostSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    author = serializers.SlugRelatedField(slug_field='user_username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'user']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
