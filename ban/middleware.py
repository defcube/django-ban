from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden
from django.conf import settings

from models import DenyIP, AllowIP

splits = lambda x: x.replace(' ','').split(',')
order = getattr(settings, 'BAN_POLICY', 'allow,deny')
opts = filter(None, splits(order)[:2])

def ip_in(ip, nets):
    for net in nets:
        if ip in net:
            return True
    return False

class Ban(object):
    def process_request(self, request):
        ip = request.META['REMOTE_ADDR']
        # HTTP_X_FORWARDED_FOR proxy fix
        if (not ip or ip == '127.0.0.1') and 'HTTP_X_FORWARDED_FOR' in request.META:
            # choose first of (possibly) multiple values
            ip = splits(request.META['HTTP_X_FORWARDED_FOR'])[0]

        deny_ips = [i.network() for i in DenyIP.objects.all()]
        allow_ips = [i.network() for i in AllowIP.objects.all()]

        allow = lambda: ip_in(ip, allow_ips)
        deny = lambda: ip_in(ip, deny_ips)

        is_banned = True
        if opts and opts[-1] == 'allow':
            is_banned = False

        if opts:
            for opt in opts:
                if opt == 'allow' and allow():
                    is_banned = False
                    break
                elif opt == 'deny' and deny():
                    is_banned = True
                    break
        else:
            if allow(): is_banned = False
            elif deny(): is_banned = True

        if is_banned:
            # delete sessions when denied
            for k in request.session.keys():
                del request.session[k]
            # returns a 403 error page, override template to customize
            return HttpResponseForbidden(render_to_string('403.html',
                        context_instance=RequestContext(request)))

