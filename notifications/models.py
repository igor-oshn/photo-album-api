from django.contrib.auth.models import User
from django.db import models


class NotificationText(models.Model):
    subject = models.CharField(max_length=255, unique=True)
    message = models.TextField()

    def __str__(self):
        return self.subject


class NotificationTopViewedPhoto(models.Model):
    status = models.BooleanField(default=False)
    send_date = models.DateField(auto_now_add=True)
    for_user = models.ForeignKey(User, on_delete=models.CASCADE)
