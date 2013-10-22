from collections import namedtuple
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist
from em.models import RouterPage, RouterPageAttribute
from em.forms import RouterPageForm


@require_GET
def detail(request, pk):
    """
    Returns information about a single router.
    """
    router_page = RouterPage.objects.prefetch_related('router').get(pk=pk)
    headers = router_page.attributes.filter(type='header').order_by('name')
    form_attrs = router_page.attributes.filter(type='form').order_by('name')
    images = router_page.attributes.filter(type='image').order_by('value')
    links = router_page.attributes.filter(type='link').order_by('value')
    try:
        router_page_title = router_page.get_title().value
    except ObjectDoesNotExist:
        router_page_title = "[Unknown or Missing]"

    return render(request, 'routerpage/detail.html',
                  {'page_title': router_page.router.model + " Page",
                   'router_page': router_page,
                   'headers': headers,
                   'form_attrs': form_attrs,
                   'images': images,
                   'links': links,
                   'router_page_title': router_page_title })

def save(request, form):
    page_title = form.instance.get_title()
    page_title.value = request.POST.get('title')
    router_page = form.save()
    page_title.router_page = router_page
    page_title.save()
    url = reverse('routerpage_detail', kwargs={'pk': router_page.pk})
    response = HttpResponse()
    response['Location'] = url
    response.status_code = 303
    return response

def create(request, router):
    if request.method == 'POST':
        form = RouterPageForm(request.POST, request.FILES)
        if form.is_valid():
            return save(request, form)
    else:
        form = RouterPageForm()
        form.fields['router'].initial = router
        template_data = {'page_title': 'New Router Page',
                         'form': form}
    return render(request, 'shared/formpage.html', template_data)


def edit(request, pk):
    routerpage = RouterPage.objects.get(pk=pk)
    if request.method == 'POST':
        form = RouterPageForm(request.POST, request.FILES, instance=routerpage)
        if form.is_valid():
            return save(request, form)
    else:
        form = RouterPageForm(instance=routerpage)
    template_data = {'page_title': routerpage.relative_url,
                     'form': form}
    return render(request, 'shared/formpage.html', template_data)


def delete(request, pk):
    return HttpResponse("Coming soon.")
