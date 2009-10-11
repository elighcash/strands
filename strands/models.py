from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.template import defaultfilters


class Strand(models.Model):
    name = models.CharField(_('name'), max_length=100, help_text="Strand name.")
    slug = models.SlugField(_('slug'), null=True, blank=True, help_text="Strand slug.")

    def save(self):
        self.slug = defaultfilters.slugify( self.name )
        super( Strand, self ).save()

    def __unicode__(self):
        return u'%s' % self.name
    
    class Admin:
        pass

class Knot(models.Model):
    author = models.ForeignKey(User)

    title = models.CharField(_('title'), max_length=100, help_text="Knot title.")
    slug = models.SlugField(_('slug'), null=True, blank=True, help_text="Knot slug (auto generated).")#models.CharField(_('slug'), max_length=100, help_text="Knot slug (for URLs).")
    blurb = models.TextField(_('blurb'), null=True, blank=True, help_text="Knot blurb. Should be first chunk of body content")
    date = models.DateTimeField(_('date published'), help_text="Date published.")
    strand_a = models.ForeignKey(Strand, related_name='strand_a')
    strand_b = models.ForeignKey(Strand, related_name='strand_b')
    body = models.TextField(_('body'), null=True, blank=True, help_text="Knot body.")
    published = models.BooleanField(_('published'), blank=True, help_text="Is knot published?")
    #threads (threaded comments)

    def save(self):
        self.slug = defaultfilters.slugify( self.title )
        super( Knot, self ).save()

    def __unicode__(self):
        return u'%s' % self.title

    class Admin:
        pass
