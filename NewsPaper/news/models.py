from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class RatingManger(models.Model):
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

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


TYPE = (
    ('Article', 'Статья'),
    ('News', 'Новость')
)


class Post(RatingManger):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=12, choices=TYPE)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=64)
    text = models.TextField()

    def preview(self):
        return f'{self.text[:124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(RatingManger):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
