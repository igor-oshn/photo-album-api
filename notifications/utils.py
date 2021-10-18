from django.core.mail import send_mail

from app import settings
from notifications.models import NotificationText, NotificationTopViewedPhoto


def send_notification(user):
    note_text = NotificationText.objects.get(subject='Top 3 Photo')
    send_mail(note_text.subject, note_text.message,
              from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[user.email])
    NotificationTopViewedPhoto.objects.create(status=True, for_user=user)
