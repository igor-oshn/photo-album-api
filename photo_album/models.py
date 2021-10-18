import os
from datetime import date
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.functional import cached_property

from notifications.models import NotificationTopViewedPhoto
from notifications.utils import send_notification
from photo_album.utils import convert_image
from photo_album.validators import validate_image

TODAY = date.today()


class PhotoQuerySet(models.QuerySet):
    def top_three_viewed_photo(self):
        return self.filter().order_by('-views')[:3]

    def top_ten_viewed_photo(self):
        return self.filter().order_by('-views')[:10]


class Photo(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos', verbose_name='User')
    photo = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png']), validate_image])
    photo_webp = models.ImageField(validators=[FileExtensionValidator(['webp'])])
    thumbnail = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png']), validate_image])
    views = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    top = PhotoQuerySet.as_manager()

    def __str__(self):
        return self.name

    def add_view(self):
        self.views += 1
        self.save(update_fields=['views'])
        top_three = Photo.top.top_three_viewed_photo()
        print(NotificationTopViewedPhoto.objects.filter(send_date=TODAY).exists())
        # Check viewed for top3
        if self.views >= top_three[top_three.count() - 1].views and \
            not NotificationTopViewedPhoto.objects.filter(send_date=TODAY).exists():
            send_notification(self.user)
        return self.views

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.convert_to_webp():
                raise Exception('Could not create webp - is the file type valid?')
            if not self.make_thumbnail():
                raise Exception('Could not create thumbnail - is the file type valid?')
        super(Photo, self).save(*args, **kwargs)

    def convert_to_webp(self):
        image_name = os.path.splitext(self.photo.name)[0]
        temp_image = convert_image(self.photo, 'webp')
        self.photo_webp.save(f'{image_name}.webp', ContentFile(temp_image.read()), save=False)
        temp_image.close()
        return True

    def make_thumbnail(self):
        thumb_name, thumb_extension = os.path.splitext(self.photo.name)
        thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_name + '_thumb' + thumb_extension
        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False
        temp_thumb = convert_image(self.photo, FTYPE, thumbnail=True)
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()
        return True


class Video(models.Model):
    name = models.CharField(max_length=255)
    video = models.FileField(upload_to='video/')
    created_at = models.DateTimeField(auto_now_add=True)
