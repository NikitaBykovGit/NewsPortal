import logging
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from news.models import Category

logger = logging.getLogger(__name__)


def my_job():
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
            subject=subject,
            body=text,
            from_email=None,
            to=subscribers_emails
        )

        msg.attach_alternative(html, "text/html")
        msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="fri",
                hour="18",
                minute="00"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
