from django.http import  HttpResponseRedirect
from django.conf import settings

def favicon_redirect(request):
    return HttpResponseRedirect('%simages/favicon.png' % settings.STATIC_URL)