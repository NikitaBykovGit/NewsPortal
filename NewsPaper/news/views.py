from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef
from django.http import HttpResponseRedirect
from .models import Author, Post, Category, Subscriber, User, Grade
from .forms import PostForm
from .filters import PostFilter
from abc import ABC


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class PostsList(ListView):
    model = Post
    ordering = "-time_in"
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class NewsList(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        if self.kwargs['type'] == 'articles':
            _type = 'Article'
        if self.kwargs['type'] == 'news':
            _type = 'News'
        queryset = super().get_queryset().filter(type=_type).order_by('-time_in')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs if self.request.GET else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['type'] == 'articles':
            page_title = 'Статьи'
        if self.kwargs['type'] == 'news':
            page_title = 'Новости'
        context['post_type'] = page_title
        print(context['post_type'])
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'news/post_search.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs if self.request.GET else Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_action'] = 'Редактирование'
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('posts_list')


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    context_object_name = 'create_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.kwargs['type'] == 'articles':
            post.type = 'Article'
        if self.kwargs['type'] == 'news':
            post.type = 'News'
        post.author = self.request.user.author
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        if self.kwargs['type'] == 'articles':
            context['page_action'] = 'Создание статьи'
        if self.kwargs['type'] == 'news':
            context['page_action'] = 'Создание новости'
        return context


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'news/subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'news/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Author.objects.filter(user_id=kwargs['object'].id).exists():
            author = User.objects.get(pk=kwargs['object'].id).author.id
            author_articles = Post.objects.filter(type='Article').filter(author_id=author)
            context['author_articles_count'] = author_articles.count()
            author_news = Post.objects.filter(type='News').filter(author_id=author)
            context['author_news_count'] = author_news.count()
        likes = Grade.objects.filter(user_id=self.kwargs['pk']).filter(grade='Like')
        context['user_likes'] = likes.count()
        dislikes = Grade.objects.filter(user_id=self.kwargs['pk']).filter(grade='Dislike')
        context['user_dislikes'] = dislikes.count()
        return context


class AddGrade(ABC, LoginRequiredMixin, View):
    def __init__(self):
        super().__init__()
        self.mark = None

    def post(self, request, pk, *args, **kwargs):
        grade = Grade.objects.filter(post_id=pk).filter(user_id=request.user.id)
        if grade.exists():
            grade.update(grade=self.mark)
        else:
            Grade.objects.create(post_id=pk, user_id=request.user.id, grade=self.mark)
        return self.back_to_page('post_detail')

    def get(self, request, *args, **kwargs):
        self.post(self.request, self.kwargs['pk'])
        return self.back_to_page('post_detail')

    def back_to_page(self, back_page):
        return HttpResponseRedirect(reverse(back_page, args=[self.kwargs['type'], self.kwargs['pk']]))


class Addlike(AddGrade):
    def __init__(self):
        super().__init__()
        self.mark = 'Like'


class AddDislike(AddGrade, LoginRequiredMixin, View):
    def __init__(self):
        super().__init__()
        self.mark = 'Dislike'