from celery import shared_task
from django.conf import settings
from templated_email import send_templated_mail


@shared_task()
def send_welcome_email_task(to):
    send_templated_mail(
        template_name='users/welcome',
        recipient_list=[to],
        from_email=settings,
        context={}
    )
