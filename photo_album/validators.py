from rest_framework.exceptions import ValidationError


def validate_image(imagefield_obj):
    filesize = imagefield_obj.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
