from django.contrib import admin
from em.models import (Router, RouterFeature, RouterPage,
                       RouterPageAttribute, RouterManager,
                       MacManufacturer, Device)

admin.site.register(Router)
admin.site.register(RouterFeature)
admin.site.register(RouterPage)
admin.site.register(RouterPageAttribute)
admin.site.register(RouterManager)
admin.site.register(MacManufacturer)
admin.site.register(Device)
