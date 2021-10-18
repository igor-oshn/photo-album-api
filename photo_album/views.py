import datetime

from django.core.files.base import ContentFile
from django.http import FileResponse
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from photo_album.models import Photo, Video
from photo_album.serializers import PhotoSerializer, EditNamePhotoSerializer
from photo_album.video import convert_top_photo_to_video


class UploadPhotoView(CreateAPIView):
    """
    Upload photo
    """
    serializer_class = PhotoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListPhotoView(ListAPIView):
    """
    Get photo list
    """
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)


class DetailPhotoView(RetrieveAPIView):
    """
    Get detail photo
    """
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.add_view()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class EditNamePhotoView(UpdateAPIView):
    """
    Edit photo's name
    """
    serializer_class = EditNamePhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)


class GetTopPhotoAllVideo(RetrieveAPIView):
    """
    Get video file (.webm) from top ten viewed photo
    """

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        today = datetime.date.today()  # date representing today's date

        if 'user' in request.query_params:
            output_filename = f'top10photo_all_{user.username}.webm'
            top_photo_path_list = [obj.photo.path for obj in Photo.top.top_ten_viewed_photo()]
        else:
            output_filename = 'top10photo_all.webm'
            top_photo_path_list = [obj.photo.path for obj in Photo.top.top_ten_viewed_photo()]

        video, created = Video.objects.get_or_create(name=output_filename)

        if created or video.created_at.date() < today:
            filepath, filename = convert_top_photo_to_video(top_photo_path_list, output_filename)
            video.video.name = f'video/{filename}'
            video.save()

        response = FileResponse(video.video.read(), content_type='video/webm')
        response['Content-Length'] = video.video.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % video.video.name

        return response
