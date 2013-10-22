import requests
from collections import namedtuple
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist
from em.models import Router, RouterPage, RouterPageAttribute
from em.forms import RouterPageForm, RouterPageAutoCreateForm
from em.libs.routers.identifier import Identifier


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


def auto_create(request, router):
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            identifier = Identifier.get_instance(url, requests.get(url))
            if identifier.parsing_succeeded():
                page = build_page_from_identifier(request, router, identifier)
                url = reverse('routerpage_detail', kwargs={'pk': page.pk})
                response = HttpResponse()
                response['Location'] = url
                response.status_code = 303
                return response
            else:
                return HttpResponse("Parsing failed")
        else:
            form = RouterPageAutoCreateForm(request.POST, request.FILES)
    else:
        form = RouterPageAutoCreateForm()
    template_data = {'page_title': 'New Router Page',
                     'form': form}
    return render(request, 'shared/formpage.html', template_data)


def build_page_from_identifier(request, router_id, identifier):
    router = Router.objects.get(pk=router_id)
    page = RouterPage(router=router)
    page.relative_url = identifier.url
    page.body = identifier.html
    page.save()

    title = page.get_title()
    title.value = identifier.title()
    title.save()

    for link in identifier.links():
        attr = RouterPageAttribute(router_page=page, type='link')
        attr.name = link['text']
        attr.value = link['href']
        attr.save()

    for form_attr in identifier.forms():
        for key in form_attr.keys():
            attr = RouterPageAttribute(router_page=page, type='form')
            attr.name = key
            attr.value = form_attr[key]
            attr.save()

    for src in identifier.images():
        attr = RouterPageAttribute(router_page=page, type='image', name='image')
        attr.value = src
        attr.save()

    for key in identifier.headers.keys():
        attr = RouterPageAttribute(router_page=page, type='header')
        attr.name = key
        attr.value = identifier.headers[key]
        attr.save()

    return page


def delete(request, pk):
    return HttpResponse("Coming soon.")
