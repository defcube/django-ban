from django.conf import settings
from django.contrib import admin
from models import DeniedIP, AllowedIP

if 'ban.middleware.DenyMiddleware' in settings.MIDDLEWARE_CLASSES:
    admin.site.register(DeniedIP)
    
if 'ban.middleware.AllowMiddleware' in settings.MIDDLEWARE_CLASSES:
    admin.site.register(AllowedIP)
