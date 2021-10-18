import os

import cv2

from app import settings
from photo_album.models import Photo


def convert_top_photo_to_video(top_photo_path_list, output_filename):
    frame_size = (1280, 720)
    output_dir = str(settings.BASE_DIR) + '/media/video/'
    os.makedirs(output_dir, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'VP90')

    filepath = output_dir + output_filename
    out = cv2.VideoWriter(filepath, fourcc, 1, frame_size)

    for filename in top_photo_path_list:
        img = cv2.imread(filename)
        img = cv2.resize(img, frame_size)
        out.write(img)
    out.release()
    return filepath, output_filename

    # self.stdout.write(self.style.SUCCESS('Successfully create video "%s%s"' % (output_dir, output_filename)))