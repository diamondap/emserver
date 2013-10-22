from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from em.models import RouterPageAttribute, RouterPage
from em.forms import DefaultFormHelper


def redirect(rpid):
    url = reverse('routerpage_detail', kwargs={'pk': rpid})
    response = HttpResponse()
    response['Location'] = url
    response.status_code = 303
    return response


def edit(request, rpid, attr_type):
    routerpage = RouterPage.objects.get(pk=rpid)
    AttrFormSet = modelformset_factory(RouterPageAttribute,
                                       fields=('name', 'value'),
                                       can_delete=True,
                                       extra=4)
    if request.method == 'POST':
        formset = AttrFormSet(request.POST)
        for form in formset:
            form.instance.router_page = routerpage
            form.instance.type = attr_type
            print(form.instance)
        if formset.is_valid():
            attrs = formset.save()
            print(attrs)
            return redirect(rpid)
    else:
        qs = RouterPageAttribute.objects.filter(
            router_page=rpid, type=attr_type).order_by('name')
        formset = AttrFormSet(queryset=qs)
    title = '{0} {1} Attributes'.format(routerpage.relative_url, attr_type)
    template_data = {'page_title': title,
                     'formset': formset,
                     'helper': DefaultFormHelper() }
    return render(request, 'shared/formsetpage.html', template_data)
