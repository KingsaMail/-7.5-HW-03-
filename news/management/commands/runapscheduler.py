import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from news.models import Post, Category

logger = logging.getLogger(__name__)


def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_added__gte=last_week)    
    categories = set(posts.values_list('categories__category', flat=True))
    emails = set(Category.objects.filter(category__in=categories).values_list('subscriptions__user__email', flat=True))
    
    
    for email in emails:
        if not email:
            continue
        posts_send = Post.objects.filter(date_added__gte=last_week, categories__subscriptions__user__email=email).distinct()
        
        html_content = render_to_string(
            'send_posts.html',
            {
                'link': 'http://127.0.0.1:8000',
                'posts': posts_send,
            }        
            )
        
        msg = EmailMultiAlternatives(
            subject = 'Статьи за неделю',
            body = '',
            from_email='',
            to=[email]
            )
        msg.attach_alternative(html_content, "text/html")
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
            trigger=CronTrigger(second="*/30"), #day_of_week="fri", hour="18", minute="00"),
            id="my_job",  # The `id` assigned to each job MUST be unique second="*/30"
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