from django.conf.urls import patterns, include, url
from em.views import api, web


api_urlpatterns = patterns(
    'emserver.em_api',

    # All of the API urls start with /api/v1
    url(r'^identify_router', api.router.identify, name='identify_router')
)

web_urlpatterns = patterns(
    'emserver.em_web',


    # Administrative pages

    # Router
    url(r'^webadmin/router/$', web.router.index, name='router_index'),
    url(r'^webadmin/router/create/$', web.router.create, name='router_create'),
    url(r'^webadmin/router/(?P<pk>\d+)/$', web.router.detail,
        name='router_detail'),
    url(r'^webadmin/router/(?P<pk>\d+)/edit/$', web.router.edit,
        name='router_edit'),
    url(r'^webadmin/router/(?P<pk>\d+)/delete/$', web.router.delete,
        name='router_delete'),

    # RouterPage
    url(r'^webadmin/routerpage/(?P<pk>\d+)/$', web.routerpage.detail,
        name='routerpage_detail'),
    url(r'^webadmin/routerpage/(?P<router>\d+)/create/$',
        web.routerpage.create,
        name='routerpage_create'),
    url(r'^webadmin/routerpage/(?P<pk>\d+)/edit/$', web.routerpage.edit,
        name='routerpage_edit'),
    url(r'^webadmin/routerpage/(?P<pk>\d+)/delete/$', web.routerpage.delete,
        name='routerpage_delete'),

    # RouterPageAttribute
    url(r'^webadmin/routerpage_attr/(?P<routerpage>\d+)/(?P<type>\w+)/create/$',
        web.routerpage_attribute.create,
        name='routerpage_attribute_create'),
    url(r'^webadmin/routerpage/(?P<routerpage>\d+)/(?P<type>\w+)/edit/$',
        web.routerpage_attribute.edit,
        name='routerpage_attribute_edit'),
    url(r'^webadmin/routerpage/(?P<pk>\d+)/delete/$',
        web.routerpage_attribute.delete,
        name='routerpage_attribute_delete'),

)
