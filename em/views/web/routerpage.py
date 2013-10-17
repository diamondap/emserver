from collections import namedtuple
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist
from em.models import RouterPage, RouterPageAttribute


@require_GET
def detail(request, pk):
    """
    Returns information about a single router.
    """
    router_page = RouterPage.objects.prefetch_related('router').get(pk=pk)
    headers = RouterPageAttribute.objects.filter(
        type='header').order_by('name')
    form_attrs = RouterPageAttribute.objects.filter(
        type='form').order_by('name')
    images = RouterPageAttribute.objects.filter(
        type='image').order_by('value')
    links = RouterPageAttribute.objects.filter(
        type='link').order_by('value')
    try:
        router_page_title = RouterPageAttribute.objects.filter(
            type='title').values('value').order_by('value').all()[0]['value']
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


def create(request):
    return HttpResponse("Coming soon.")

def edit(request, pk):
    return HttpResponse("Coming soon.")

def delete(request, pk):
    return HttpResponse("Coming soon.")
