from django.db import models
from django.template import defaultfilters
from django.conf import settings

from license.models import License
from location.models import Location
from profile.models import Profile




RESERVED_WORDS = ('about', 'admin', 'knot', 'manage', 'strands', 'author')

from utils import *


# CORE CONTENT
#####################################################################
class Strand(models.Model):
    """
    A topic, like a tag, with name, slug, and description.
    """
    name = models.CharField(max_length=100, help_text="Strand name.")
    slug = models.SlugField(blank=True, unique=True, help_text="Strand slug.")
    description = models.TextField(blank=True, help_text="Optional description, definition, or other info about the strand.")

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
    """
    The post object. Has various data associated with it, including references to one or more authors, exactly two strands, one or more locations, and a license. Also includes settings and other metadata, like notes.
    """
    authors = models.ManyToManyField(Profile, related_name="author_knots", help_text="Authors of post.")

    title = models.CharField(max_length=44, help_text="Post title.")
    tagline = models.CharField(max_length=160, blank=True, help_text="Post tagline, a short, catchy sentence.")
    blurb = models.CharField(max_length=250, blank=True, help_text="Post blurb, a quick overview.")
    thumbnail = models.FileField(upload_to=get_media_upload_to, blank=True, help_text="Thumbnail for post.")

    slug = models.SlugField(blank=True, unique=True, help_text="Post slug (auto generated).")
    short_url = models.CharField(max_length=100, blank=True, unique=True, help_text="Short link for sharing.")

    date = models.DateTimeField(help_text="Date published.")
    strand_a = models.ForeignKey(Strand, related_name='strand_a')
    strand_b = models.ForeignKey(Strand, related_name='strand_b')

    body = models.TextField(blank=True, help_text="Post body.")
    style = models.TextField(blank=True, help_text="Post style (JSON string).")

    notes = models.TextField(blank=True, help_text="Post notes.")
    published = models.BooleanField(blank=True, help_text="Is post published?")
    allow_comments = models.BooleanField(help_text="Can people comment?")
    location = models.ManyToManyField(Location, null=True, blank=True, related_name="location", help_text="Associated locations.")
    license = models.ForeignKey(License, null=True, blank=True, related_name="license", help_text="License applied to post.")
    
    def save(self):
        if not self.slug:
            slug = defaultfilters.slugify( self.title )
            try:
                existing = Knot.objects.filter(slug=slug)
            except Knot.DoesNotExist:
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

    def get_share_url(self):
        manager = Manager.objects.all()[0]
        domain = manager.short_url_domain if manager.short_url_domain else 'localhost:8000'
        path = '/' + self.short_url if self.short_url else self.get_absolute_url()
        return 'http://' + domain + path

    def style_css(self):
        style = simplejson.loads(self.style)
        css = ''
        #add in @font-face rules as necessary
        for selector in style['rules']:
            css = css + '#k' + str(self.id) + ' ' + selector + ' {'
            for property in style['rules'][selector]:
                css = css + ' ' + property + ': ' + style['rules'][selector][property] + '; '
            css = css + '} '
        return css




# SITE MANAGEMENT SETTINGS
#####################################################################
class Manager(models.Model):
    """
    The manager class allows for various information and defaults to
    be set, without needing access to admin. (This will allow for a
    more user-friendly and STRANDS-specific settings page that still
    needs to be built.)
    """
    
    allow_attachments = models.BooleanField(default=True, help_text="Are attachments allowed?")
    allow_images = models.BooleanField(default=True, help_text="Are images allowed?")
    allow_locations = models.BooleanField(default=True, help_text="Are locations allowed?")
    allow_fonts = models.BooleanField(default=True, help_text="Are custom fonts allowed?")
    allow_rss = models.BooleanField(default=True, help_text="Are RSS feeds allowed?")
    allow_comments = models.BooleanField(default=True, help_text="Are comments allowed?")

    default_styles = models.TextField(blank=True, help_text="Default styles for knots (JSON string).")
    knot_comments_default = models.BooleanField(default=True, help_text="Default for knot comments setting.")
    license_default = models.ForeignKey(License, null=True, blank=True, help_text="Default license for posts.")

    publisher_name = models.CharField(max_length=200, blank=True, help_text="Publisher name (for copyright).")

    site_title = models.CharField(max_length=200, default='A STRANDS site', help_text="Site title.")
    short_url_domain = models.CharField(max_length=200, help_text="Domain ( e.g. example.com ) of the short URL redirect.")


    def __unicode__(self):
        return u'%s' % self.site_title
