from django.core.urlresolvers import reverse
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from em import models

class DefaultFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(DefaultFormHelper, self).__init__(*args, **kwargs)
        self.add_input(Button('cancel', 'Cancel',
                              css_class="btn-default",
                              style="float:left"))
        self.add_input(Submit('submit', 'Submit', style="float:right"))



class RouterForm(forms.ModelForm):

    features = forms.ModelMultipleChoiceField(
        models.RouterFeature.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False)

    def __init__(self, *args, **kwargs):
        super(RouterForm, self).__init__(*args, **kwargs)
        self.helper = DefaultFormHelper()
        self.helper.form_id = 'router-form'
        self.helper.form_method = 'post'
        feature_dict = {}
        if self.instance and self.instance.pk:
            for feature in self.instance.features.all():
                feature_dict[feature.pk] = True
            self.fields['features'].initial = feature_dict

    class Meta:
        model = models.Router
