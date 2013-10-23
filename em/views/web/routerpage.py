import requests
from collections import namedtuple
from django.http import HttpResponse
from django.shortcuts import render, redirect
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
    return render(request, 'routerpage/detail.html',
                  {'page_title': router_page.router.model + " Page",
                   'router_page': router_page,
                   'headers': router_page.get_headers(),
                   'form_attrs': router_page.get_form_attributes(),
                   'images': router_page.get_images(),
                   'links': router_page.get_links(),
                   'scripts': router_page.get_scripts(),
                   'form_fields': router_page.get_form_fields(),
                   'router_page_title': router_page.get_title() })

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
    router_page = RouterPage.objects.get(pk=pk)
    if request.method == 'POST':
        form = RouterPageForm(request.POST, request.FILES, instance=router_page)
        if form.is_valid():
            return save(request, form)
    else:
        form = RouterPageForm(instance=router_page)
    template_data = {'page_title': router_page.relative_url,
                     'form': form}
    return render(request, 'shared/formpage.html', template_data)


def auto_create(request, router):
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            identifier = Identifier.get_instance(
                url, requests.get(url, timeout=3))
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

    for script in identifier.scripts():
        attr = RouterPageAttribute(
            router_page=page, type='script', name='script')
        attr.value = script
        attr.save()

    for form_attr in identifier.form_attrs():
        for key in form_attr.keys():
            attr = RouterPageAttribute(router_page=page, type='form_attr')
            attr.name = key
            attr.value = form_attr[key]
            attr.save()

    for src in identifier.images():
        attr = RouterPageAttribute(
            router_page=page, type='image_src', name='image_src')
        attr.value = src
        attr.save()

    for key in identifier.headers.keys():
        attr = RouterPageAttribute(router_page=page, type='header')
        attr.name = key
        if identifier.headers[key]:
            attr.value = identifier.headers[key][0:250]
        attr.save()

    for element in identifier.form_elements():
        attr = RouterPageAttribute(router_page=page)
        attr.type = element['type']
        attr.name = element['name']
        if element['value'] is not None:
            attr.value = element['value'][0:250]
        attr.save()

    return page


def delete(request, pk):
    if request.method == 'POST':
        router_page = RouterPage.objects.get(pk=pk)
        router = router_page.router
        router_page.delete()
        return redirect('router_detail', pk=router.pk)
    else:
        router_page = RouterPage.objects.get(pk=pk)
        template_data = {'page_title': 'Delete Router Page',
                         'object_name': router_page.relative_url }
        return render(request, 'shared/delete.html', template_data)
