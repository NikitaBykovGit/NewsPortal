from django.contrib import admin
from .models import Author, Category, PostCategory, Comment

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)
