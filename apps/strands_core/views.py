from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import  HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson
from models import *
import re, os, random


def home(request, template_name="home.html.django"):
    knots = Knot.objects.filter(published=True).order_by("-date")
    return render_to_response(template_name, {
        "knots": knots,
        }, context_instance=RequestContext(request))

#display all knots
def tapestry(request, template_name="tapestry.html.django"):
    knots = Knot.objects.filter(published=True)
    if request.session.get('is_mobile', True):
        strands = None
        knots = knots.order_by("-date")
        num_strands = None
    else:
        strands = Strand.objects.all()
        num_strands = strands.count()
    return render_to_response(template_name, {
        "strands": strands,
        "num_strands": num_strands,
        "knots": knots
        }, context_instance=RequestContext(request))

#display this particular knot
def display_knot(request, knot_slug, template_name="knot.html.django"):
    if request.user.is_staff:
        knot = get_object_or_404(Knot, slug=knot_slug)
    else:
        knot = get_object_or_404(Knot, slug=knot_slug, published=True)

    return render_to_response(template_name, {
        "knot": knot,
        }, context_instance=RequestContext(request))


def display_knot_short(request, knot_short):
    knot_short = knot_short.strip('_-.,\)>]/ ')
    slug = get_object_or_404(Knot, short_url = knot_short).slug
    return HttpResponseRedirect(reverse('poll_results', args=(slug,)))

