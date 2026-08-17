from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_event_registration_email(user_email, event_title):
    subject = f"Event Registration: {event_title}"
    message = f'Congratulations! You have successfully registered for the event "{event_title}".'

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
