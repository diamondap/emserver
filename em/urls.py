from django.conf.urls import patterns, include, url
from em.views.api import router

api_urlpatterns = patterns(
    'emserver.em_api',

    url(r'^identify_router', router.identify, name='identify-router')
)

web_urlpatterns = patterns(
    'emserver.em_web',

)
