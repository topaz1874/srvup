from django.forms import ModelForm
from .models import Video,Category

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Submit,Button
from crispy_forms.bootstrap import FormActions

class VidForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'embed_code', 'category']
        # exclude = ['']

    def __init__(self, *args, **kwargs):
        super(VidForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'vidForm'
        self.helper.form_class = 'vidClass'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Submit('cancel', 'Cancel'))

        # self.helper.layout = Layout(
        #     FormActions(
        #             Submit('save', 'Save changes'),
        #             Button('cancel', 'Cancel')
        #             ))



