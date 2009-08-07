from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import  HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings
from models import *

#The following two methods, tapestry and display_strand, will eventually become
#a single view that controls the tapestry visualization that allows for display
#and organization of all knots.

#display all knots
def tapestry(request):
    strands = Strand.objects.all()
    template_name = "tapestry.django.html"
    return render_to_response(template_name, {
        "strands": strands,
        }, context_instance=RequestContext(request))

#display all knots with these a and b strands
#currently, intersecting strands (specifying both a and b) is not supported
def display_strand(request, strand_a_name="$none", strand_b_name="$none"):
    strand_a = Strand.objects.get(name = strand_a_name)
    knots_a = strand_a.strand_a.all()
    knots_b = strand_a.strand_b.all()
    template_name = "strand.django.html"
    return render_to_response(template_name, {
        "knots_a": knots_a,
        "knots_b": knots_b,
        "strand_a": strand_a,
        #"strand_b":strand_b,
        }, context_instance=RequestContext(request))

#display this particular knot
def display_knot(request, knot_slug):
    knot = Knot.objects.get(slug = knot_slug)
    template_name = "knot.django.html"
    return render_to_response(template_name, {
        "knot": knot,
        }, context_instance=RequestContext(request))

#display all knots written by author
def display_by_author(request, author_username):
    author = User.objects.get(username = author_username)
    knots = author.knot_set.all()
    template_name = "author.django.html"
    return render_to_response(template_name, {
        "author": author,
        "knots": knots,
        }, context_instance=RequestContext(request))

#display the three most recent posts
def index(request):
    template_name = "index.django.html"
    latest_knots = Knot.objects.all().order_by("-id")[:3]
    return render_to_response(template_name, {
        "latest_knots": latest_knots,
        }, context_instance=RequestContext(request))
