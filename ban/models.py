
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
try:
    from ipcalc import Network
except ImportError:
    raise ImproperlyConfigured('You must install ipcalc >= 0.1')

class IP(models.Model):
    ip = models.CharField(_('IP network'), max_length=18,
            help_text=_('Either IP address or IP network specification'))
    
    def __unicode__(self):
        return self.ip

    def network(self):
        return Network(self.ip)
        
    class Meta:
        abstract = True
        verbose_name = _('IP address')
        verbose_name_plural = _('IP adresses')
        
class DenyIP(IP): pass
class AllowIP(IP): pass