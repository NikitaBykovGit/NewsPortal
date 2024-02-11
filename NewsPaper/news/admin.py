from django.contrib import admin
from .models import Author, Category, PostCategory, Comment, Post
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostTranslationAdmin(TranslationAdmin):
    model = Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_category', 'time_in', 'type')
    list_filter = ('author', 'time_in', 'category')
    search_fields = ('title', 'author__user__username')


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
