from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse


class RatingManger(models.Model):
    rating = models.IntegerField(default=0)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text}'

    class Meta:
        abstract = True


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.post_set.all().aggregate(Sum('rating')).get('rating__sum')
        comments_rating = self.user.comment_set.all().aggregate(Sum('rating')).get('rating__sum') or 0
        com_to_posts = Comment.objects.all().filter(user=self.user).aggregate(Sum('rating')).get('rating__sum') or 0
        self.rating = posts_rating * 3 + comments_rating + com_to_posts
        self.save()

    def __str__(self):
        return self.user.username


CATEGORY = (
    ('Internet', 'Интернет'),
    ('Culture', 'Культура'),
    ('Science', 'Наука'),
    ('Society', 'Общество'),
    ('Policy', 'Политика'),
    ('Crime', 'Преступления'),
    ('Incidents', 'Происшествия'),
    ('Religion', 'Религия'),
    ('Sport', 'Спорт'),
    ('Economy', 'Экономика')
)


class Category(models.Model):
    name = models.CharField(max_length=12, choices=CATEGORY, default='Internet', unique=True)

    def __str__(self):
        return self.name


TYPE = (
    ('Article', 'Статья'),
    ('News', 'Новость')
)


class Post(RatingManger):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=12, choices=TYPE)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=64)

    def preview(self):
        return f'{self.text[:124]}...'

    def get_absolute_url(self):
        if self.type == 'News':
            _type = 'news'
        elif self.type == 'Article':
            _type = 'articles'
        return reverse('post_detail', args=[_type, str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

    def update_rating(self):
        likes = Grade.objects.filter(post_id=self.pk).filter(grade='Like').count()
        dislikes = Grade.objects.filter(post_id=self.pk).filter(grade='Dislike').count()
        self.rating = likes - dislikes
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(RatingManger):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscriptions')


GRADE = (
    ('Like', 1),
    ('Dislike', -1)
)


class Grade(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=7, choices=GRADE, default='Like')
