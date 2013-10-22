from django.conf.urls import patterns, include, url
import em.views.api.router as api_router
import em.views.web.router as web_router
import em.views.web.routerpage as web_routerpage

api_urlpatterns = patterns(
    'emserver.em_api',

    # All of the API urls start with /api/v1
    url(r'^identify_router', api_router.identify, name='identify_router')
)

web_urlpatterns = patterns(
    'emserver.em_web',


    # Administrative pages

    # Router
    url(r'^webadmin/router/$', web_router.index, name='router_index'),
    url(r'^webadmin/router/create/$', web_router.create, name='router_create'),
    url(r'^webadmin/router/(?P<pk>\d+)/$', web_router.detail,
        name='router_detail'),
    url(r'^webadmin/router/(?P<pk>\d+)/edit/$', web_router.edit,
        name='router_edit'),
    url(r'^webadmin/router/(?P<pk>\d+)/delete/$', web_router.delete,
        name='router_delete'),

    # RouterPage
    url(r'^webadmin/routerpage/(?P<pk>\d+)/$', web_routerpage.detail,
        name='routerpage_detail'),
    url(r'^webadmin/routerpage/create/$', web_routerpage.create,
        name='routerpage_create'),
    url(r'^webadmin/routerpage/(?P<pk>\d+)/edit/$', web_routerpage.edit,
        name='routerpage_edit'),
    url(r'^webadmin/routerpage/(?P<pk>\d+)/delete/$', web_routerpage.delete,
        name='routerpage_delete'),

)
