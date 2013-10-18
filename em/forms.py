from django.core.urlresolvers import reverse
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from em.models import Router

class DefaultFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(DefaultFormHelper, self).__init__(*args, **kwargs)
        self.add_input(Button('cancel', 'Cancel',
                              css_class="btn-default",
                              style="float:left"))
        self.add_input(Submit('submit', 'Submit', style="float:right"))



class RouterForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(RouterForm, self).__init__(*args, **kwargs)
        self.helper = DefaultFormHelper()
        self.helper.form_id = 'router-form'
        self.helper.form_method = 'post'
        #self.helper.form_action = reverse('router-edit')

    class Meta:
        model = Router
