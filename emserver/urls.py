from django.conf.urls import patterns, include, url
from django.contrib import admin
from em.urls import api_urlpatterns, web_urlpatterns
from emserver import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^api/v1/', include(api_urlpatterns)),
    url(r'', include(web_urlpatterns)),
)

if settings.ADMIN_ENABLED:
    urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)))
