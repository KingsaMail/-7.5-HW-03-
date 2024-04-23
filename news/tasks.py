import datetime
from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Category, Post

@shared_task
def send_to_users(subject, text_content, html_content, emails):
    
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    
@shared_task
def action_every_monday_8am():
    
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_added__gte=last_week)    
    categories = set(posts.values_list('categories__category', flat=True))
    emails = set(Category.objects.filter(category__in=categories).values_list('subscriptions__user__email', flat=True))
    
    
    for email in emails:
        if not email:
            continue
        posts_send = Post.objects.filter(date_added__gte=last_week,
                                         categories__subscriptions__user__email=email,
                                         ).distinct()
        
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
    