from collections import namedtuple
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from em.libs.form_handler import FormHandler
from em.models import Router
from em.forms import RouterForm
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
    sort_by = [request.GET.get('sort')]
    if sort_by[0] is None:
        sort_by = ['manufacturer', 'model', 'firmware_version']

    values_list = ['id', 'manufacturer', 'model', 'firmware_version',
                   'modified']

    routers = Router.objects.values_list(*values_list).order_by(*sort_by)
    router_filter = RouterFilter(request.GET, queryset=routers)
    filtered_routers = router_filter.qs

    return render(request, 'router/index.html',
                  {'page_title': 'Routers',
                   'table_summary': 'List of Routers',
                   'object_type': 'router',
                   'tuples': filtered_routers,
                   'filter_form': router_filter.form })

@require_GET
def detail(request, pk):
    """
    Returns information about a single router.
    """
    router = Router.objects.prefetch_related('features', 'pages').get(pk=pk)
    return render(request, 'router/detail.html',
                  {'page_title': router.model,
                   'router': router })

def save(request, form):
    router = form.save()
    router.features.clear()
    for feature in request.POST.getlist('features'):
        router.features.add(feature)
    router.save()
    url = reverse('router_detail', kwargs={'pk': router.pk})
    response = HttpResponse()
    response['Location'] = url
    response.status_code = 303
    return response


def create(request):
    if request.method == 'POST':
        form = RouterForm(request.POST, request.FILES)
        if form.is_valid():
            return save(request, form)
    else:
        form = RouterForm()
        template_data = {'page_title': 'New Router',
                         'form': form}
    return render(request, 'shared/formpage.html', template_data)


def edit(request, pk):
    router = Router.objects.get(pk=pk)
    if request.method == 'POST':
        form = RouterForm(request.POST, request.FILES, instance=router)
        if form.is_valid():
            return save(request, form)
    else:
        form = RouterForm(instance=router)
    template_data = {'page_title': router.model,
                     'form': form}
    return render(request, 'shared/formpage.html', template_data)


def delete(request, pk):
    return HttpResponse("Coming soon.")
