from django.conf import settings
from django.http import  HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def favicon_redirect(request):
    return HttpResponseRedirect('%simages/favicon.png' % settings.STATIC_URL)

def toggle_mobile(request):
    request.session['is_mobile'] = not request.session.get('is_mobile', True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('home')))


from strands_core.models import Knot

def sitemap(request, template_name="sitemap.xml.django"):
    knots = Knot.objects.filter(published=True).order_by("-date")
    return render_to_response(template_name, {
        "knots": knots,
        }, context_instance=RequestContext(request))