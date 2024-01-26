from celery import shared_task
from datetime import datetime
from .models import Category, Post
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_email_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    subscribers_emails = []

    for cat in categories:
        subscribes = cat.subscriptions.all()
        subscribers_emails += [s.user.email for s in subscribes]

    subject = 'Новый пост:'
    text = f'{post.title}'
    html = (
        f'<a href="http://127.0.0.1:8000/{post.type.lower()}/{post.id}">{post.title}</a>'
    )
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=None,
        to=subscribers_emails
    )

    msg.attach_alternative(html, "text/html")
    msg.send()


@shared_task
def weekly_send_email_task():
    categories = Category.objects.all()
    subscribers_emails = []

    data = datetime.now()

    for cat in categories:
        subscribes = cat.subscriptions.all()
        subscribers_emails += [s.user.email for s in subscribes]
        posts = cat.post_set.all()

        subject = f'Новые посты на тему: {cat} за неделю'
        text = ''
        html = ('')
        for post in posts:
            delta = data.date() - post.time_in.date()
            if delta.days < 7:
                text += f'{post.title} {post.time_in.date()}\n'
                html += (f'<a href="http://127.0.0.1:8000/{post.type.lower()}/{post.id}">{post.title}</a>'
                         f'{post.time_in.date()}') + '\n'

        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=subscribers_emails
        )

        msg.attach_alternative(html, "text/html")
        msg.send()
