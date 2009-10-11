from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib import admin

# Strands are the organizing construct of the CMS. They function in the same manner as tags or topics.
# Each Knot is associated with two strands.
class Strand(models.Model):
    name = models.CharField(_('name'), max_length=100, help_text="Strand name.")

    def __unicode__(self):
        return u'%s' % self.name


# Knots are the core content structure of the CMS. Each knot has an author and two strands associated
# with it. They also contain a title, slug, date, and body.
#
# Currently, the slug needs to be input manually and must be url-safe.
# The slug can be anything, but having a url friendly version of the title is reccommended.
# Todo: have the slug be created automatically from the title.
class Knot(models.Model):
    author = models.ForeignKey(User)

    title = models.CharField(_('title'), max_length=100, help_text="Knot title.")
    slug = models.CharField(_('slug'), max_length=100, help_text="Knot slug (for URLs).")
    date = models.DateTimeField(_('date published'), help_text="Date published.")
    strand_a = models.ForeignKey(Strand, related_name='strand_a')
    strand_b = models.ForeignKey(Strand, related_name='strand_b')
    body = models.TextField(_('body'), null=True, blank=True, help_text="Knot body.")

    def __unicode__(self):
        return u'%s' % self.title


admin.site.register(Knot)
admin.site.register(Strand)