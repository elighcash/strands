from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from strands.models import Strand, Knot


def index(request, template_name = "index.django.html"):
    latest_knots = Knot.objects.filter(published = True).order_by("-id")[:3]
    return direct_to_template(request, template_name, extra_context={"latest_knots": latest_knots})

#display all knots
def tapestry(request, template_name="tapestry.django.html"):
    return direct_to_template(request, template_name, extra_context={"strands": Strand.objects.all()})

#display all knots with these a and b strands
def display_strand(request, strand_a_slug="$none", strand_b_slug="$none", ordera="-date", orderb="title", template_name="strand.django.html"):
    strand_a = get_object_or_4040(slug=strand_a_slug)
    knots_a = strand_a.strand_a.filter(published=True).order_by(ordera)
    knots_b = strand_a.strand_b.filter(published=True).order_by(orderb)
    #if strand_b_id != "$none":
    #    strand_b = Strand.objects.get(name = strand_b_id)
    #    knots = knots.filter(strand_b = strand_b_id)
    #else:
    #    strand_b = "$none"
    return direct_to_template(request, template_name,
            extra_context={"knots_a": knots_a,
                           "knots_b": knots_b,
                           "strand_a": strand_a,
                           #"strand_b":strand_b,
                           })

def display_knot(request, knot_slug, template_name="knot.django.html"):
    knot = get_object_or_404(slug=knot_slug, published=True)
    return direct_to_template(request, template_name, extra_context={"knot": knot})

def display_by_author(request, author_username, order="title", template_name="author.django.html"):
    author = get_object_or_404(username=author_username)
    knots = author.knot_set.filter(published = True).order_by(order)
    oti, osa, osb, oda = "", "", "", ""
    if order == "title":
        oti = "-"
    if order == "strand_a":
        osa = "-"
    if order == "strand_b":
        osb = "-"
    if order == "date":
        oda = "-"
    return direct_to_template(request, template_name,
            extra_context={"author": author,
                           "knots": knots,
                           "oti": oti,
                           "osa": osa,
                           "osb": osb,
                           "oda": oda,
                           })

#def display_by_date(request, date_slug, order="title", template_name="author.django.html"):
#    date = User.objects.get(username=author_username)
#    knots = author.knot_set.all().order_by(order)
#    oti, osa, osb, oda = "", "", "", ""
#    if order == "title":
#        oti = "-"
#    if order == "strand_a":
#        osa = "-"
#    if order == "strand_b":
#        osb = "-"
#    if order == "date":
#        oda = "-"
#    return direct_to_template(request, template_name,
#            extra_context={"author": author,
#                           "knots": knots,
#                           "oti": oti,
#                           "osa": osa,
#                           "osb": osb,
#                           "oda": oda,
#                           })
