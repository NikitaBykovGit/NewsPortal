from django.contrib.auth.models import User

from .models import Post, Author
from rest_framework import serializers


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Author
        fields = ['user']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


