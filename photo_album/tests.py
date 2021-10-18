from django.contrib.auth.models import User
from django.http import FileResponse
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from notifications.models import NotificationText
from photo_album.models import Photo
from photo_album.utils import generate_photo_file


def create_notification_text():
    if not NotificationText.objects.filter(subject='Top 3 Photo').exists():
        NotificationText.objects.create(subject="Top 3 Photo",
                                        message="Your photo was in the top 3 most viewed")


class UserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        generate_photo_file()
        cls.user = User.objects.create(username='Test', is_active=True)
        cls.user.set_password('Azds213123')
        cls.user.save()
        cls.token = Token.objects.create(user=cls.user)
        cls.photo_file = generate_photo_file()

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        create_notification_text()
        photo_name = 'Test_setup'
        photo = Photo.objects.create(name=photo_name, photo=self.photo_file.name, user=self.user)
        photo.save()

    def test_upload_photo(self):
        """
        Test if we can upload a photo
        """
        url = reverse('photo:upload')
        data = {'name': 'Test', 'photo': self.photo_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_upload_photo_without_name(self):
        """
        Test if we can't upload a photo without name
        """
        url = reverse('photo:upload')
        data = {'name': '', 'photo': self.photo_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_photo_without_photo(self):
        """
        Test if we can't upload a photo without name
        """
        url = reverse('photo:upload')
        data = {'name': 'Test', 'photo': ''}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_photo_list(self):
        """
        Test we can get all photo.
        """
        url = reverse('photo:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Photo.objects.count(), 1)

    def test_edit_photo_name(self):
        """
        Test we can edit photo name.
        """
        url = reverse('photo:edit', args=[1])
        data = {'name': 'Test_edit'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Photo.objects.get(id=1).name, 'Test_edit')

    def test_edit_photo_name_invalid(self):
        """
        Test we can't edit photo without name.
        """
        url = reverse('photo:edit', args=[1])
        data = {'name': ''}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Photo.objects.get(id=1).name, 'Test_setup')

    def test_get_detail_photo(self):
        """
        Test we can get detail photo.
        """
        url = reverse('photo:detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Photo.objects.get(id=1).name, 'Test_setup')

    def test_get_top_photo_all(self):
        """
        Test we can get top10 photo webm file.
        """
        url = reverse('photo:top-ten-photo')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response), type(FileResponse()))

    def test_get_top_photo_user(self):
        """
        Test we can get top10 photo's user webm file.
        """
        url = reverse('photo:top-ten-photo')
        response = self.client.get(url, {'user': ''})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response), type(FileResponse()))
