from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse


class FormHandler:

    ENC_TYPE_URL_ENCODED = 'application/x-www-form-urlencoded'
    ENC_TYPE_MULTIPART   = 'multipart/form-data'

    def __init__(self, form_class, model_class, redirect_action,
                 form_template='shared/formpage.html', template_data={}):
        self.form_class = form_class
        self.form_template = form_template
        self.model_class = model_class
        self.redirect_action = redirect_action
        self.model_instance = None
        self.form_instance = None
        self.action = None
        self.template_data = template_data
        self.enc_type = FormHandler.ENC_TYPE_URL_ENCODED

    def handle_get(self, request, model_instance=None):
        self.action = 'EDIT' if model_instance else 'CREATE'
        if model_instance:
            self.model_instance = model_instance
            self.form_instance = self.form_class(instance=self.model_instance)
        else:
            self.form_instance = self.form_class()
        return True

    def handle_post(self, request, model_instance=None):
        if model_instance:
            self.action = 'EDIT'
            self.model_instance = model_instance
            self.form_instance = self.form_class(
                request.POST, request.FILES,
                instance=self.model_instance)
        else:
            self.action = 'CREATE'
            self.form_instance = self.form_class(request.POST, request.FILES)
        return self.form_instance.is_valid()

    def create_or_edit(self, request, pk=None):
        """
        Handles all of the form-related work for editing a model instance.
        Renders an empty form for create or a bound form for edit.
        """
        if request.method == 'GET':
            self.handle_get(request, pk)
        else:
            if self.handle_post(request, pk):
                return self.post_succeeded(request)
        return self.render_form(request)

    def post_succeeded(self, request):
        """
        To be called when a post to a /create/ or /edit/ url succeeds.
        This saves the created/edited object and returns a redirect
        with the Location header set to whatever URL maps to redirect_action.
        """
        obj = self.form_instance.save()
        url = reverse(self.redirect_action, kwargs={'pk': obj.pk})
        response = HttpResponse()
        response['Location'] = url
        response.status_code = 303
        return response

    def render_form(self, request):
        data = {'form': self.form_instance,
                'action': self.action,
                'enc_type': self.enc_type}
        self.template_data.update(data)
        return render(request, self.form_template, self.template_data)
