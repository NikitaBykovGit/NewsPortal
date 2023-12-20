from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render
from .models import Post
from .forms import PostForm
from .filters import PostFilter


class PostsList(ListView):
    model = Post
    ordering = "-time_in"
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class NewsList(ListView):
    model = Post
    ordering = "-time_in"
    template_name = 'news/news.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_create.html'
    context_object_name = 'create_post'


class PostSearch(ListView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_search.html'
    context_object_name = 'filtered_posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context
