from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit

class CommentForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Your comment or reply',})
        )
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        # self.helper.add_input(Submit('submit', 'Add Comment', css_class='btn btn-primary',))

        self.helper.layout = Layout(
            'text',
            ButtonHolder(
                Submit('submit', 'Add Comment', css_class='btn-primary'),
                )
            )