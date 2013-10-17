from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse


class FormHandler:

    ENC_TYPE_URL_ENCODED = 'application/x-www-form-urlencoded'
    ENC_TYPE_MULTIPART   = 'multipart/form-data'

    def __init__(self, form_class, model_class, redirect_action,
                 form_template = 'shared/formpage.html'):
        self.form_class = form_class
        self.form_template = form_template
        self.model_class = model_class
        self.redirect_action = redirect_action
        self.model_instance = None
        self.form_instance = None
        self.action = None
        self.enc_type = FormHandler.ENC_TYPE_URL_ENCODED

    def handle_get(self, request, id):
        self.action = 'EDIT' if id else 'CREATE'
        if id:
            self.model_instance = get_object_or_404(self.model_class, pk=id)
            self.form_instance = self.form_class(
                instance=self.model_instance, session_user=request.user)
        else:
            self.form_instance = self.form_class(session_user=request.user)
        return True

    def handle_post(self, request, id):
        if id:
            self.action = 'EDIT'
            self.model_instance = get_object_or_404(self.model_class, pk=id)
            self.form_instance = self.form_class(
                request.POST, request.FILES,
                instance=self.model_instance,
                session_user=request.user)
        else:
            self.action = 'CREATE'
            self.form_instance = self.form_class(
                request.POST, request.FILES, session_user=request.user)
        return self.form_instance.is_valid()

    def create_or_edit(self, request, id=None):
        """
        Handles all of the form-related work for editing a model instance.
        Renders an empty form for create or a bound form for edit.
        """
        if request.method == 'GET':
            self.handle_get(request, id)
        else:
            if self.handle_post(request, id):
                return self.post_succeeded(request)
        return self.render_form(request)

    def post_succeeded(self, request):
        """
        To be called when a post to a /create/ or /edit/ url succeeds.
        This saves the created/edited object and returns a redirect
        with the Location header set to whatever URL maps to redirect_action.
        """
        obj = self.form_instance.save()
        url = reverse(self.redirect_action, kwargs={'id': obj.id})
        response = HttpResponse()
        response['Location'] = url
        response.status_code = 303
        return response

    def render_form(self, request):
        return render(request, self.form_template,
                      {'form': self.form_instance,
                       'action': self.action,
                       'enc_type': self.enc_type})
