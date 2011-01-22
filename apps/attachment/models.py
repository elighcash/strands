from django.db import models

from strands_core.models import Knot

from utils import get_media_upload_to

class Attachment(models.Model):
    """
    Used for attachments to a post - e.g. code snippets, extra
    images, etc.
    """
    
    knot = models.ForeignKey(Knot, related_name="attachments", help_text="Knot to attach to.")
    name = models.CharField(max_length=100, blank=True, help_text="Attachment name.")
    file = models.FileField(upload_to=get_media_upload_to, help_text="File to attach.")
    description = models.TextField(blank=True, help_text="Attachment description.")

    def __unicode__(self):
        return u'%s' % str(self.file)[22:]
