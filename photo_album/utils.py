import io
import os
from io import BytesIO

import cv2
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile

from app import settings


def convert_image(instance, extension, thumbnail=False):
    image = Image.open(instance).convert("RGB")
    if thumbnail:
        image.thumbnail((150, 150), Image.ANTIALIAS)
    temp_image = BytesIO()
    image.save(temp_image, extension)
    temp_image.seek(0)
    return temp_image


def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    default_storage.save(file.name, file)
    return SimpleUploadedFile(file.name, file.getvalue())


# image_list = Photo.objects.order_by('views')[0:10]
# print(image_list)
# top_photo_path_list = [obj.photo.path for obj in Photo.objects.filter().order_by('views')[0:10]]


