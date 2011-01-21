from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from django.contrib.syndication.feeds import Feed
from models import Knot, Strand
from django.contrib.auth.models import User

class all_knots(Feed):
    title = "All Knots"
    link = "/"
    description = "All Knots"

    def items(self):
        return Knot.objects.order_by('-date')
    
    def item_pubdate(self, knot):
        return knot.date

    def item_description(self, knot):
        return knot.body

class latest_knots(Feed):
    title = "Latest Knots"
    link = "/"
    description = "The Latest Knots"

    def items(self):
        return Knot.objects.order_by('-date')[:5]
    
    def item_pubdate(self, knot):
        return knot.date

class author_feed(Feed):
    def get_object(self, bits):
        # In case of "/rss/beats/0613/foo/bar/baz/", or other such clutter,
        # check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username=bits[0])

    def title(self, user):
        return "Knots by %s" % user.first_name

    def link(self, user):
        if not user:
            raise FeedDoesNotExist
        return "http://example.com/author/" + user.username#strand.get_absolute_url()

    def description(self, user):
        return "Knots posted by %s" % user.first_name

    def items(self, user):
        return Knot.objects.filter(author=user).order_by('-date')

    def item_pubdate(self, knot):
        return knot.date

