from django.conf.urls import patterns, include, url
import em.views.api.router as api_router
import em.views.web.router as web_router

api_urlpatterns = patterns(
    'emserver.em_api',

    # All of the API urls start with /api/v1
    url(r'^identify_router', api_router.identify, name='identify-router')
)

web_urlpatterns = patterns(
    'emserver.em_web',


    # These are administrative pages
    url(r'^webadmin/router', web_router.index, name='router-index')
)
