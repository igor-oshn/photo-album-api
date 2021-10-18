from django.forms import ImageField
from rest_framework import serializers

from photo_album.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'name', 'photo', 'photo_webp', 'thumbnail', 'uploaded_at', 'views')
        extra_kwargs = {'id': {'read_only': True},
                        'photo_webp': {'read_only': True},
                        'thumbnail': {'read_only': True},
                        'uploaded_at': {'read_only': True},
                        'views': {'read_only': True}}


class EditNamePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('name',)
