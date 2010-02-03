from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden
from django.conf import settings

from models import DeniedIP, AllowedIP

def ip_in(ip, model):
    """
    Returns True if the given ip address is in one of the ban models
    """
    for i in model.objects.all():
        if ip in i.network():
            return True
    return False

def get_ip(request):
    """
    Gets the true client IP address of the request
    Contains proxy handling involving HTTP_X_FORWARDED_FOR and multiple addresses
    """
    ip = request.META['REMOTE_ADDR']
    if (not ip or ip == '127.0.0.1') and 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    return ip.replace(',','').split()[0] # choose first of (possibly) multiple values

def forbid(request):
    """
    Forbids a user to access the site
    Cleans up their session (if it exists)
    Returns a templated HttpResponseForbidden when banning requests
    Override the `403.html` template to customize the error report
    """
    for k in request.session.keys():
        del request.session[k]
    return HttpResponseForbidden(render_to_string('403.html',
                context_instance=RequestContext(request)))
    
class DenyMiddleware(object):
    """
    Forbids any request if they are in the DeniedIP list
    """
    def process_request(self, request):
        if ip_in(get_ip(request), DeniedIP):
            return forbid(request)

class AllowMiddleware(object):
    """
    Forbids any request if they are not in the AllowedIP list
    """
    def process_request(self, request):
        if not ip_in(get_ip(request), AllowedIP):
            return forbid(request)