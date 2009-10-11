from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import  HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.conf import settings
from models import *

#display all knots
def tapestry(request):
    strands = Strand.objects.all()
    template_name = "tapestry.django.html"
    return render_to_response(template_name, {
        "strands": strands,
        }, context_instance=RequestContext(request))

#display all knots with these a and b strands
def display_strand(request, strand_a_slug="$none", strand_b_slug="$none", ordera="-date", orderb="title"):
    try:
        strand_a = Strand.objects.get(slug = strand_a_slug)
    except Strand.DoesNotExist:
        raise Http404
    knots_a = strand_a.strand_a.filter(published = True).order_by(ordera)
    knots_b = strand_a.strand_b.filter(published = True).order_by(orderb)
    #if strand_b_id != "$none":
    #    strand_b = Strand.objects.get(name = strand_b_id)
    #    knots = knots.filter(strand_b = strand_b_id)
    #else:
    #    strand_b = "$none"
    template_name = "strand.django.html"
    return render_to_response(template_name, {
        "knots_a": knots_a,
        "knots_b": knots_b,
        "strand_a": strand_a,
        #"strand_b":strand_b,
        }, context_instance=RequestContext(request))

#display this particular knot
def display_knot(request, knot_slug):
    try:
        knot = Knot.objects.get(slug = knot_slug, published = True)
    except Knot.DoesNotExist:
        raise Http404
    template_name = "knot.django.html"
    return render_to_response(template_name, {
        "knot": knot,
        }, context_instance=RequestContext(request))

def display_by_author(request, author_username, order="title"):
    try:
        author = User.objects.get(username = author_username)
    except User.DoesNotExist:
        raise Http404
    knots = author.knot_set.filter(published = True).order_by(order)
    template_name = "author.django.html"
    oti = ""
    osa = ""
    osb = ""
    oda = ""
    if order == "title":
        oti = "-"
    if order == "strand_a":
        osa = "-"
    if order == "strand_b":
        osb = "-"
    if order == "date":
        oda = "-"
    return render_to_response(template_name, {
        "author": author,
        "knots": knots,
        "oti": oti,
        "osa": osa,
        "osb": osb,
        "oda": oda,
        }, context_instance=RequestContext(request))

#def display_by_date(request, date_slug, order="title"):
#    date = User.objects.get(username = author_username)
#    knots = author.knot_set.all().order_by(order)
#    template_name = "author.django.html"
#    oti = ""
#    osa = ""
#    osb = ""
#    oda = ""
#    if order == "title":
#        oti = "-"
#    if order == "strand_a":
#        osa = "-"
#    if order == "strand_b":
#        osb = "-"
#    if order == "date":
#        oda = "-"
#    return render_to_response(template_name, {
#        "author": author,
#        "knots": knots,
#        "oti": oti,
#        "osa": osa,
#        "osb": osb,
#        "oda": oda,
#        }, context_instance=RequestContext(request))

def index(request):
    template_name = "index.django.html"
    latest_knots = Knot.objects.filter(published = True).order_by("-id")[:3]
    return render_to_response(template_name, {
        "latest_knots": latest_knots,
        }, context_instance=RequestContext(request))
