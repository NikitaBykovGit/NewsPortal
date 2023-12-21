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

    def get_queryset(self):
        return Post.objects.filter(type='News').order_by('-time_in')


class ArticlesList(ListView):
    model = Post
    ordering = "-time_in"
    template_name = 'news/articles.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(type='Article').order_by('-time_in')


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'
    context_object_name = 'create_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'News'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/article_edit.html'
    context_object_name = 'create_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'Article'
        return super().form_valid(form)



class PostSearch(ListView):
    model = Post
    template_name = 'news/post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs if self.request.GET else Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context
