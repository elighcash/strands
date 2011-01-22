from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import Profile

def display_profile(request, profile_slug, template_name="author.html.django"):
    return render_to_response(template_name, {
        "author": get_object_or_404(Profile, slug=profile_slug)
        }, context_instance=RequestContext(request))

