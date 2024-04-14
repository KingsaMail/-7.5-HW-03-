from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver

from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    
    if kwargs['action'] == 'post_add':
        
        emails = User.objects.filter(
            subscriptions__category__in=instance.categories.all().values_list('id', flat=True)
        ).values_list('email', flat=True)
        
        emails = list(set(emails))
        
        subject = f'Новая статья (новость) в категории {", ".join(instance.categories.all().values_list("category", flat=True))}'
        
        text_content = (
            f'Статья (новость): {instance.title}\n'
            f'анонс: {instance.preview()}\n\n'
            f'Ссылка на статью (новость): http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        
        html_content = (
        f'Статья (новость): {instance.title}<br>'
        f'анонс: {instance.preview()}<br><br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на статью (новость)</a>'
        )
        
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send() 
    