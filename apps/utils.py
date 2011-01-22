from django.conf import settings

import random, string, math
import os.path


def get_media_upload_to(instance, filename):
    return os.path.join(settings.MEDIA_ROOT, 'uploads', instance.knot.slug, filename)

def random_alphanumeric(count):
    return [random.choice(string.letters + string.digits) for i in range(count)]

