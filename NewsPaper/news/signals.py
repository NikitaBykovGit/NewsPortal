# from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import send_email_task


# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         subscribers_emails = []
#
#         for cat in categories:
#             subscribes = cat.subscriptions.all()
#             subscribers_emails += [s.user.email for s in subscribes]
#
#         subject = f'Новый пост:'
#         text = f'{instance.title}'
#         html = (
#             f'<a href="http://127.0.0.1:8000/{instance.type.lower()}/{instance.id}">{instance.title}</a>'
#         )
#         msg = EmailMultiAlternatives(
#             subject=subject,
#             body=text,
#             from_email=None,
#             to=subscribers_emails
#         )
#
#         msg.attach_alternative(html, "text/html")
#         msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        send_email_task(instance.pk)
