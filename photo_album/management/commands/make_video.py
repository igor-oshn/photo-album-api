import os

import cv2
from django.core.management.base import BaseCommand, CommandError

from app import settings
from photo_album.models import Photo


class Command(BaseCommand):
    help = 'Making video(.webm) from top 10 viewed photos'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        frame_size = (1280, 720)
        output_dir = str(settings.BASE_DIR) + '/media/video/'
        output_filename = 'top10photo_all.webm'
        os.makedirs(output_dir, exist_ok=True)

        fourcc = cv2.VideoWriter_fourcc(*'VP90')
        out = cv2.VideoWriter(output_dir+output_filename, fourcc, 1, frame_size)

        top_photo_path_list = [obj.photo.path for obj in Photo.objects.filter().order_by('-views')[0:10]]
        for filename in top_photo_path_list:
            img = cv2.imread(filename)
            img = cv2.resize(img, frame_size)
            out.write(img)
        out.release()

        self.stdout.write(self.style.SUCCESS('Successfully create video "%s%s"' % (output_dir, output_filename)))