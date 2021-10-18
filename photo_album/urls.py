from django.urls import path
from photo_album.views import UploadPhotoView, ListPhotoView, DetailPhotoView, EditNamePhotoView, GetTopPhotoAllVideo


app_name = 'photo'
urlpatterns = [
    path('top/', GetTopPhotoAllVideo.as_view(), name='top-ten-photo'),
    path('upload/', UploadPhotoView.as_view(), name='upload'),
    path('list/', ListPhotoView.as_view(), name='list'),
    path('<pk>/', DetailPhotoView.as_view(), name='detail'),
    path('edit/<pk>/', EditNamePhotoView.as_view(), name='edit'),
]
