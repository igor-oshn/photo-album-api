import os

import cv2
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from app import settings
from notifications.models import NotificationText
from photo_album.models import Photo
from photo_album.utils import generate_photo_file


def create_user():
    if not User.objects.filter(username='User1').exists():
        user = User.objects.create(username='User1', email='user1@example.com', is_active=True)
        user.set_password('Azds213123')
        user.save()
        token = Token.objects.create(user=user)
    else:
        user = User.objects.get(username='User1')
    return user


def create_notification_text():
    if not NotificationText.objects.filter(subject='Top 3 Photo').exists():
        notification = NotificationText.objects.create(subject="Top 3 Photo",
                                                   message="Your photo was in the top 3 most viewed")


class Command(BaseCommand):
    help = 'Generate data for models'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        user = create_user()
        create_notification_text()
        print(user)
        image_file = generate_photo_file()
        for i in range(0, 10):
            photo_obj = Photo.objects.create(name=f"Image_{i}", photo=image_file, user=user)
            photo_obj.save()
            self.stdout.write(self.style.SUCCESS('Successfully create photo instance %s' % photo_obj.name))
