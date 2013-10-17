from collections import namedtuple
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from em.models import Router
import django_filters


FilterTuple = namedtuple('FilterTuple', ['field', 'display'])

class RouterFilter(django_filters.FilterSet):
    manufacturer = django_filters.CharFilter(lookup_type='icontains')
    model = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = Router
        fields = ['manufacturer', 'model']

@require_GET
def index(request):
    """
    Returns a list of routers.
    """
    sort = request.GET.get('sort')
    if sort:
        order_by = [sort]
    else:
        order_by = ['manufacturer', 'model', 'firmware_version']

    values_list = ['id', 'manufacturer', 'model', 'firmware_version',
                   'modified']

    routers = Router.objects.values_list(*values_list).order_by(*order_by)

    available_filters = [
        FilterTuple('manufacturer', 'Manufacturer'),
        FilterTuple('model', 'Model'),]

    router_filter = RouterFilter(request.GET, queryset=routers)
    filtered_routers = router_filter.qs



    return render(request, 'router/index.html',
                  {'page_title': 'Routers',
                   'table_summary': 'List of Routers',
                   'object_type': 'router',
                   'supports_new' : True,
                   'supports_edit': True,
                   'supports_delete': True,
                   'tuples': filtered_routers,
                   'filter_options': available_filters,
                   'filter': router_filter })
