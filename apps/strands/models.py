from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.template import defaultfilters
from django.conf import settings

from utils import random_alphanumeric

import math
import os.path


RESERVED_WORDS = ['about', 'admin', 'knot', 'manage', 'strands', 'author', 'feeds']

def get_media_upload_to(instance, filename):
    location = os.path.join(settings.MEDIA_ROOT, 'uploads', instance.knot.slug, filename)
    return location



###### META INFORMATION

# License class allows specific licenses to be defined site-wide, which can then be applied to knots when posted. The knot's license is automatically rendered in the template, so that it's searchable.
class License(models.Model):
    name = models.CharField(_('name'), max_length=100, blank=True, help_text="License name (e.g. Creative Commons Attribution-Share Alike).")
    abbreviation = models.CharField(_('abbreviation'), max_length=200, blank=True, help_text="License abbreviation (e.g. CC BY-SA).")
    description = models.TextField(_('description'), blank=True, help_text="License description.")
    code_url = models.URLField(_('license code url'), blank=True, help_text="URL of license code.") #prefer url?
    code = models.TextField(_('license code text'), blank=True, help_text="License code.")

    def __unicode__(self):
        return self.name


# Locations are used by authors and knots. None of the fields are required, so a location can be just geo coordinates, just a name, or any combination of fields.
class Location(models.Model):
    name = models.CharField(_('name'), max_length=255, blank=True, help_text="Location name.")
    address = models.CharField(_('address'), max_length=255, blank=True, help_text="Location address.")
    city = models.CharField(_('city'), max_length=255, blank=True, help_text="City.")
    region = models.CharField(_('region'), max_length=255, blank=True, help_text="Region.")
    postal_code = models.CharField(_('postalcode'), max_length=255, blank=True, help_text="Postal code.")
    latitude = models.FloatField(_('latitude'), blank=True)
    longitude = models.FloatField(_('longitude'), blank=True)


# Authors have profiles which provide information for their profile page, as well as meta data on individual knot pages.
class AuthorProfile(models.Model):
    user = models.ForeignKey(User, related_name="profile", help_text="Associated User")
    bio = models.TextField(_('bio'), blank=True, help_text="Author bio.")
    image = models.FileField(upload_to="images/", help_text="Author image.") #should be imagefield
    url = models.URLField(_('url'), blank=True, help_text="Author URL.")
    location = models.ForeignKey(Location, null=True, blank=True, help_text="Author location.")
    twitter_name = models.CharField(_('twitter name'), blank=True, max_length=15, help_text="Author Twitter screen name (no @).")

    def __unicode__(self):
        return u'%s' % self.user.username

    def save(self):
        super( AuthorProfile, self ).save()




###### CORE CONTENT

class Strand(models.Model):
    name = models.CharField(_('name'), max_length=100, help_text="Strand name.")
    slug = models.SlugField(_('slug'), blank=True, unique=True, help_text="Strand slug.")
    description = models.TextField(_('description'), blank=True, help_text="Optional description, definition, or other info about the strand.")

    def save(self):
        slug = defaultfilters.slugify( self.name )
        strands = Strand.objects.filter(slug=slug)
        if strands.count() == 0:
            self.slug = slug
        else:
            self.slug = "%s-%s" % (slug, str(strands.count() + 1))
        super( Strand, self ).save()

    def get_absolute_url(self):
        return ('display_strand', [str(self.slug)])
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return u'%s' % self.name


class Knot(models.Model):
    author = models.ManyToManyField(User, related_name="author_knots", help_text="Authors of post.")

    title = models.CharField(_('title'), max_length=44, help_text="Post title.")
    slug = models.SlugField(_('slug'), blank=True, unique=True, help_text="Post slug (auto generated).")
    short_url = models.CharField(_('short'), max_length=100, blank=True, help_text="Short link for sharing.")
    tagline = models.CharField(_('tagline'), max_length=160, blank=True, help_text="Post tagline, a short, catchy sentence.")
    blurb = models.CharField(_('blurb'), max_length=250, blank=True, help_text="Post blurb, a quick overview.")
    date = models.DateTimeField(_('date published'), help_text="Date published.")
    strand_a = models.ForeignKey(Strand, related_name='strand_a')
    strand_b = models.ForeignKey(Strand, related_name='strand_b')
    body = models.TextField(_('body'), blank=True, help_text="Post body.")
    style = models.TextField(_('style'), blank=True, help_text="Post style (JSON string).")
    notes = models.TextField(_('notes'), blank=True, help_text="Post notes.")
    published = models.BooleanField(_('published'), blank=True, help_text="Is post published?")
    allow_comments = models.BooleanField(_('allow comments'), help_text="Can people comment?")
    allow_rss = models.BooleanField(_('allow rss'), help_text="Can the knot be included in RSS feeds?")
    location = models.ManyToManyField(Location, null=True, blank=True, related_name="location", help_text="Associated locations.")
    license = models.ForeignKey(License, null=True, blank=True, related_name="license", help_text="License applied to post.")
    
    def save(self):
        if not self.slug:
            slug = defaultfilters.slugify( self.title )
            try:
                existing = Knot.objects.get(slug=slug)
            except Knot.DoesNotExist:
                pass
            else:
                slug = '%s-%s' % (slug, (existing.count() + 1))
            self.slug=slug
        while not self.short_url:
            count = Knot.objects.count()
            if count < 1:
                count = 1
            short_url = ''.join(random_alphanumeric(int(math.log(count,62))+1))
            if short_url not in RESERVED_WORDS:
                try:
                    existing = Knot.objects.get(short_url=short_url)
                except Knot.DoesNotExist:
                    self.short_url = short_url
        super( Knot, self ).save()

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return ('display_knot', [str(self.slug)])
    get_absolute_url = models.permalink(get_absolute_url)




###### EXTRA CONTENT

# Used for attachments to a post - e.g. code snippets, extra images, etc.
class Attachment(models.Model):
    knot = models.ForeignKey(Knot, related_name="attachments", help_text="Knot to attach to.")
    name = models.CharField(_('name'), max_length=100, blank=True, help_text="Attachment name.")
    file = models.FileField(upload_to=get_media_upload_to, help_text="File to attach.")
    description = models.TextField(_('description'), blank=True, help_text="Attachment description.")

    def __unicode__(self):
        return u'%s' % str(self.file)[22:]

# Later - fonts, images, etc (once Loom editor is built)


###### SITE MANAGEMENT SETTINGS - not really used yet

# The manager class allows for various information and defaults to be set, without needing access to admin. (This will allow for a more user-friendly and STRANDS-specific settings page that still needs to be built.)
class Manager(models.Model):
    allow_attachments = models.BooleanField(_('allow attachments'), default=True, help_text="Are attachments allowed?")
    allow_images = models.BooleanField(_('allow images'), default=True, help_text="Are images allowed?")
    allow_locations = models.BooleanField(_('allow locations'), default=True, help_text="Are locations allowed?")
    allow_fonts = models.BooleanField(_('allow fonts'), default=True, help_text="Are custom fonts allowed?")
    allow_rss = models.BooleanField(_('allow rss'), default=True, help_text="Are RSS feeds allowed?")
    allow_comments = models.BooleanField(_('allow comments'), default=True, help_text="Are comments allowed?")
    default_styles = models.TextField(_('default styles'), blank=True, help_text="Default styles for knots (JSON string).")
    knot_rss_default = models.BooleanField(_('knot rss default'), default=True, help_text="Default for knot rss setting.")
    knot_comments_default = models.BooleanField(_('allow attachments'), default=True, help_text="Default for knot comments setting.")
    license_default = models.ForeignKey(License, null=True, blank=True, help_text="Default license for posts.")
    publisher_name = models.CharField(_('publisher name'), max_length=200, blank=True, help_text="Publisher name (for copyright).")
    site_title = models.CharField(_('site title'), max_length=200, default='A STRANDS site', help_text="Site title.")
    short_url_domain = models.CharField(_('short_url_domain'), max_length=200, help_text="Domain ( e.g. example.com ) of the short URL redirect.")
    editors = models.ManyToManyField(User, blank=True, null=True, related_name="manager_editors", help_text="Users who can edit any post by default.")
    managers = models.ManyToManyField(User, blank=True, null=True, related_name="manager_managers", help_text="Users who can manage the site.")
    

    def __unicode__(self):
        return u'%s' % self.site_title

    def can_manage(self, user):
        for manager in self.managers.all():
            if user == manager:
                return True
        return False

    def can_edit(self, user):
        for editor in self.editors.all():
            if user == editor:
                return True
        return False

