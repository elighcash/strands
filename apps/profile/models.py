from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from location.models import Location

import os.path

def get_author_image_upload_to(instance, filename):
    return os.path.join(settings.MEDIA_ROOT, 'images', instance.user.username, filename)

class Profile(models.Model):
    """
    Authors have profiles which provide information for their profile page, as well as meta data on individual knot pages.
    """
    user = models.ForeignKey(User, related_name="profile", help_text="Associated User")
    bio = models.TextField(blank=True, help_text="Author bio.")
    image = models.FileField(blank=True, null=True, upload_to=get_author_image_upload_to, help_text="Author image.") #should be imagefield
    url = models.URLField(blank=True, help_text="Author URL.")
    location = models.ForeignKey(Location, null=True, blank=True, help_text="Author location.")
    twitter_name = models.CharField(blank=True, max_length=15, help_text="Author Twitter screen name (no @).")
    name = models.CharField(blank=True, max_length=100, help_text="")
    slug = models.CharField(blank=True, max_length=100, help_text="")

    def __unicode__(self):
        return u'%s' % self.user.username

    def save(self):
        if not self.slug:
            slug = slugify( self.name )
            print slug
            try:
                existing = Profile.objects.get(slug=slug)
            except Profile.DoesNotExist:
                self.slug=slug
        super( Profile, self ).save()