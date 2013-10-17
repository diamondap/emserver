from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from em.models import Router

@require_GET
def index(request):
    """
    Returns a list of routers.
    """
    values_list = ['id', 'manufacturer', 'model', 'firmware_version',
                   'modified']
    order_by = ['manufacturer', 'model', 'firmware_version']
    routers = Router.objects.values_list(*values_list).order_by(*order_by)

    return render(request, 'router/index.html',
                  {'page_title': 'Routers',
                   'table_summary': 'List of Routers',
                   'object_type': 'router',
                   'supports_new' : True,
                   'supports_edit': True,
                   'tuples': routers,
                   #'filter_options': available_filters,
                   'supports_delete': True })

    return HttpResponse("OK")
